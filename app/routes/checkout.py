from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import current_user, login_required
from app.services.cart_service import CartService
from app.services.checkout_service import CheckoutService
from app.models.user import Address
from app import db
from decimal import Decimal

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

@checkout_bp.route('/payment/<int:order_id>')
@login_required
def payment(order_id):
    from app.models.order import Order
    from app.services.payment_service import PaymentService
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        return redirect(url_for('index'))
    
    # Create Preference for Card and SDK data for PIX
    preference = PaymentService.create_preference(order)
    
    # For PIX, we can also pre-create or wait for user to click
    # Let's pass the preference ID and public key to the template
    return render_template('checkout/payment.html', 
                           order=order, 
                           preference_id=preference.get('id'),
                           public_key=current_app.config['MP_PUBLIC_KEY'])

@checkout_bp.route('/webhook', methods=['POST'])
def webhook():
    from app.services.payment_service import PaymentService
    data = request.get_json()
    if data:
        PaymentService.process_webhook(data)
    return '', 200

@checkout_bp.route('/pix/<int:order_id>')
@login_required
def get_pix(order_id):
    from app.models.order import Order
    from app.services.payment_service import PaymentService
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        return {'error': 'Unauthorized'}, 403
        
    payment = PaymentService.create_pix_payment(order)
    
    return {
        'qr_code': payment.get('point_of_interaction', {}).get('transaction_data', {}).get('qr_code'),
        'qr_code_base64': payment.get('point_of_interaction', {}).get('transaction_data', {}).get('qr_code_base64'),
        'copy_paste': payment.get('point_of_interaction', {}).get('transaction_data', {}).get('qr_code')
    }

@checkout_bp.route('/success/<int:order_id>')
@login_required
def success(order_id):
    return render_template('checkout/success.html', order_id=order_id)
