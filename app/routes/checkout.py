import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import current_user, login_required
from app.services.cart_service import CartService
from app.services.checkout_service import CheckoutService
from app.models.user import Address
from app import db
from decimal import Decimal

logger = logging.getLogger(__name__)

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/')
@login_required
def index():
    items, subtotal = CartService.get_cart_data(current_user)
    if not items:
        flash('Seu carrinho está vazio.', 'warning')
        return redirect(url_for('cart.index'))
    
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    # Pass subtotal to check for free shipping
    shipping_res = CheckoutService.calculate_shipping(None, subtotal)
    shipping_cost = shipping_res['cost']
    total = Decimal(str(subtotal)) + shipping_cost
    
    return render_template('checkout/index.html', 
                           items=items, 
                           subtotal=subtotal, 
                           addresses=addresses, 
                           shipping_cost=shipping_cost, 
                           total=total)

@checkout_bp.route('/validate_coupon', methods=['POST'])
@login_required
def validate_coupon():
    code = request.form.get('code')
    _, subtotal = CartService.get_cart_data(current_user)
    
    coupon, discount = CheckoutService.validate_coupon(code, Decimal(str(subtotal)))
    
    if coupon:
        return jsonify({
            'status': 'success',
            'discount': float(discount),
            'coupon_id': coupon.id,
            'message': f'Cupom {coupon.code} aplicado!'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': discount # discount contains error message when coupon is None
        })

@checkout_bp.route('/process', methods=['POST'])
@login_required
def process():
    address_id = request.form.get('address_id')
    coupon_id = request.form.get('coupon_id')
    discount_amount = Decimal(request.form.get('discount_amount', '0.00'))
    zip_code = request.form.get('zip_code') # For shipping calculation
    
    if not address_id:
        # Handle new address creation here if needed
        street = request.form.get('street')
        number = request.form.get('number')
        neighborhood = request.form.get('neighborhood')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        
        if not all([street, number, neighborhood, city, state, zip_code]):
            flash('Por favor, selecione ou preencha um endereço completo.', 'danger')
            return redirect(url_for('checkout.index'))
            
        new_address = Address(
            user_id=current_user.id,
            street=street,
            number=number,
            neighborhood=neighborhood,
            city=city,
            state=state,
            zip_code=zip_code
        )
        db.session.add(new_address)
        db.session.commit()
        address_id = new_address.id
    else:
        # Get zip_code from existing address if not provided
        addr = Address.query.get(address_id)
        if addr:
            zip_code = addr.zip_code

    _, subtotal = CartService.get_cart_data(current_user)
    shipping_res = CheckoutService.calculate_shipping(zip_code, subtotal)
    shipping_cost = shipping_res['cost']
    
    order, error = CheckoutService.create_order(
        current_user, 
        address_id, 
        shipping_cost, 
        coupon_id=coupon_id if coupon_id else None, 
        discount_amount=discount_amount
    )
    
    if error:
        flash(error, 'danger')
        return redirect(url_for('cart.index'))
        
    return redirect(url_for('checkout.payment', order_id=order.id))

@checkout_bp.route('', methods=['POST'])
@login_required
def create_checkout():
    """Endpoint oficial: POST /checkout

    Cria a preferência do Checkout Pro a partir do pedido informado e
    redireciona o usuário para o checkout hospedado pelo Mercado Pago.

    Espera um 'order_id' de um pedido já criado (via /checkout/process) pertencente
    ao usuário autenticado.
    """
    from app.models.order import Order

    order_id = request.form.get('order_id') or request.args.get('order_id')
    order = Order.query.get_or_404(order_id) if order_id else None

    if not order or order.user_id != current_user.id:
        logger.error("Tentativa de checkout com order_id inválido ou não pertencente ao usuário: %s", order_id)
        flash('Pedido inválido.', 'danger')
        return redirect(url_for('cart.index'))

    return redirect(url_for('checkout.payment', order_id=order.id))

@checkout_bp.route('/payment/<int:order_id>')
@login_required
def payment(order_id):
    from app.models.order import Order
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:
        return redirect(url_for('public.home'))

    if not current_app.config.get('PAYMENTS_ENABLED'):
        logger.info(
            "Pagamentos em modo homologação (PAYMENTS_ENABLED=false) — exibindo showcase para o pedido #%s.",
            order_id
        )
        return redirect(url_for('checkout.showcase', order_id=order.id))

    from app.services.payment_service import PaymentService

    # Checkout Pro oficial: cria a preferência com os itens do pedido
    preference = PaymentService.create_preference(order)

    init_point = preference.get('init_point') if preference else None
    if not init_point:
        logger.error("Não foi possível obter o init_point do Mercado Pago para o pedido #%s.", order_id)
        flash('Não foi possível iniciar o pagamento. Tente novamente em instantes.', 'danger')
        return redirect(url_for('cart.index'))

    # Redireciona o usuário para o Checkout Pro oficial do Mercado Pago
    return redirect(init_point)

@checkout_bp.route('/preparando/<int:order_id>')
@login_required
def showcase(order_id):
    """Página de homologação exibida enquanto a conta oficial do Mercado Pago
    ainda não foi vinculada. O pedido já foi criado normalmente (fica 'pending'),
    apenas a cobrança real é adiada."""
    from app.models.order import Order
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:
        return redirect(url_for('public.home'))

    return render_template('checkout/showcase.html', order=order)

@checkout_bp.route('/webhook', methods=['POST'])
def webhook():
    from app.services.payment_service import PaymentService
    data = request.get_json(silent=True)
    if not data:
        logger.error("Webhook do Mercado Pago recebido sem corpo JSON válido.")
        return '', 200
    try:
        PaymentService.process_webhook(data)
    except Exception:
        logger.error("Erro inesperado ao processar webhook do Mercado Pago. Payload: %s", data, exc_info=True)
    return '', 200

@checkout_bp.route('/success')
def success():
    order_id = request.args.get('external_reference')
    status = request.args.get('status') or request.args.get('collection_status')
    logger.info("Retorno de sucesso do Mercado Pago. order_id=%s status=%s", order_id, status)
    return render_template('checkout/success.html', order_id=order_id)

@checkout_bp.route('/failure')
def failure():
    order_id = request.args.get('external_reference')
    status = request.args.get('status') or request.args.get('collection_status')
    logger.error("Retorno de falha do Mercado Pago. order_id=%s status=%s", order_id, status)
    return render_template('checkout/failure.html', order_id=order_id)

@checkout_bp.route('/pending')
def pending():
    order_id = request.args.get('external_reference')
    status = request.args.get('status') or request.args.get('collection_status')
    logger.info("Retorno de pendência do Mercado Pago. order_id=%s status=%s", order_id, status)
    return render_template('checkout/pending.html', order_id=order_id)
