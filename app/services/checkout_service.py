import json
import urllib.request
from app import db
from app.models.order import Order, OrderItem
from app.models.user import Address
from app.services.cart_service import CartService
from decimal import Decimal

class CheckoutService:
    @staticmethod
    def calculate_shipping(zip_code, subtotal=Decimal('0.00')):
        """
        Calculates shipping based on Brazilian regions using ViaCEP API for accuracy.
        """
        if not zip_code:
            return {'cost': Decimal('0.00'), 'days': '0', 'region': 'N/A'}

        # Clean CEP
        zip_code = ''.join(filter(str.isdigit, str(zip_code)))
        if len(zip_code) != 8:
            return {'cost': Decimal('0.00'), 'days': '0', 'region': 'Inválido'}

        subtotal = Decimal(str(subtotal))
        
        # Get region info from ViaCEP
        res = CheckoutService._get_region_info_via_cep(zip_code)
        
        if res['region'] == 'Inválido':
            return res

        # Free shipping: orders >= R$ 499
        if subtotal >= Decimal('499.00'):
            return {'cost': Decimal('0.00'), 'days': res['days'], 'region': res['region'], 'free': True}

        return res

    @staticmethod
    def _get_region_info_via_cep(zip_code):
        try:
            url = f"https://viacep.com.br/ws/{zip_code}/json/"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            if 'erro' in data:
                return {'cost': Decimal('0.00'), 'days': '0', 'region': 'Inválido'}
            
            uf = data.get('uf', '')
            
            norte = ['AC','AP','AM','PA','RO','RR','TO']
            nordeste = ['AL','BA','CE','MA','PB','PE','PI','RN','SE']
            centro = ['DF','GO','MT','MS']
            sudeste = ['SP','RJ','MG','ES']
            sul = ['PR','RS','SC']
            
            if uf in norte:
                return {'cost': Decimal('34.90'), 'days': '8 a 12', 'region': uf}
            elif uf in nordeste:
                return {'cost': Decimal('29.90'), 'days': '5 a 8', 'region': uf}
            elif uf in centro:
                return {'cost': Decimal('27.90'), 'days': '4 a 7', 'region': uf}
            elif uf in sudeste:
                return {'cost': Decimal('19.90'), 'days': '2 a 5', 'region': uf}
            elif uf in sul:
                return {'cost': Decimal('24.90'), 'days': '3 a 6', 'region': uf}
                
        except Exception as e:
            print(f"Error fetching shipping info: {e}")
            
        # Fallback to old digit-based logic if API fails
        return CheckoutService._get_region_info_fallback(zip_code)

    @staticmethod
    def _get_region_info_fallback(zip_code):
        first_digit = int(zip_code[0])
        if first_digit >= 0 and first_digit <= 3:
            return {'cost': Decimal('19.90'), 'days': '2 a 5', 'region': 'Sudeste (Est.)'}
        elif first_digit >= 8: # Corrigindo para Nordeste/Norte aproximado
            return {'cost': Decimal('29.90'), 'days': '5 a 12', 'region': 'Norte/Nordeste (Est.)'}
        return {'cost': Decimal('25.00'), 'days': '5 a 10', 'region': 'Brasil'}

    @staticmethod
    def validate_coupon(code, subtotal):
        from app.models.cms import Coupon
        coupon = Coupon.query.filter_by(code=code.upper(), is_active=True).first()
        
        if not coupon:
            return None, "Cupom inválido ou expirado."
        
        discount = Decimal('0.00')
        if coupon.discount_type == 'percentage':
            discount = subtotal * (coupon.value / Decimal('100.00'))
        else:
            discount = coupon.value
            
        return coupon, discount

    @staticmethod
    def create_order(user, address_id, shipping_cost, coupon_id=None, discount_amount=Decimal('0.00')):
        items, subtotal = CartService.get_cart_data(user)
        if not items:
            return None, "Carrinho vazio"

        total = Decimal(str(subtotal)) + shipping_cost - discount_amount
        if total < 0: total = Decimal('0.00')
        
        order = Order(
            user_id=user.id,
            status='pending',
            total_amount=total,
            shipping_cost=shipping_cost,
            discount_amount=discount_amount,
            coupon_id=coupon_id,
            shipping_address_id=address_id
        )
        db.session.add(order)
        db.session.flush() # Get order ID before commit

        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price_at_time=Decimal(str(item['price']))
            )
            db.session.add(order_item)

        # Clear cart after order creation
        from app.models.cart import Cart, CartItem
        cart = Cart.query.filter_by(user_id=user.id).first()
        if cart:
            CartItem.query.filter_by(cart_id=cart.id).delete()
        
        db.session.commit()
        return order, None

    @staticmethod
    def prepare_payment_payload(order):
        """Prepares data for a payment gateway (e.g., Stripe, Mercado Pago)."""
        return {
            'order_id': order.id,
            'amount': float(order.total_amount),
            'currency': 'BRL',
            'items': [
                {
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'price': float(item.price_at_time)
                } for item in order.items
            ]
        }
