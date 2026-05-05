from app import db
from app.models.order import Order, OrderItem
from app.models.user import Address
from app.services.cart_service import CartService
from decimal import Decimal

class CheckoutService:
    @staticmethod
    def calculate_shipping(zip_code):
        """Mock shipping calculation logic."""
        # In a real app, integrate with Correios or other API
        return Decimal('25.00')

    @staticmethod
    def create_order(user, address_id, shipping_cost):
        items, subtotal = CartService.get_cart_data(user)
        if not items:
            return None, "Carrinho vazio"

        total = Decimal(str(subtotal)) + shipping_cost
        
        order = Order(
            user_id=user.id,
            status='pending',
            total_amount=total,
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
