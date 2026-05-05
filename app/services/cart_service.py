from app import db
from app.models.cart import Cart, CartItem
from app.models.product import Product
from flask import session

class CartService:
    @staticmethod
    def get_cart_data(user=None):
        """Returns a list of items with product details and subtotal."""
        items_data = []
        total = 0
        
        if user and user.is_authenticated:
            cart = Cart.query.filter_by(user_id=user.id).first()
            if cart:
                for item in cart.items:
                    product = item.product
                    subtotal = product.price * item.quantity
                    items_data.append({
                        'product_id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'quantity': item.quantity,
                        'image_url': product.image_url,
                        'subtotal': float(subtotal)
                    })
                    total += subtotal
        else:
            session_cart = session.get('cart', {})
            for product_id, quantity in session_cart.items():
                product = Product.query.get(int(product_id))
                if product:
                    subtotal = product.price * quantity
                    items_data.append({
                        'product_id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'quantity': quantity,
                        'image_url': product.image_url,
                        'subtotal': float(subtotal)
                    })
                    total += subtotal
        
        return items_data, float(total)

    @staticmethod
    def add_to_cart(product_id, quantity=1, user=None):
        if user and user.is_authenticated:
            cart = Cart.query.filter_by(user_id=user.id).first()
            if not cart:
                cart = Cart(user_id=user.id)
                db.session.add(cart)
                db.session.commit()
            
            item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
            if item:
                item.quantity += quantity
            else:
                item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
                db.session.add(item)
            db.session.commit()
        else:
            cart = session.get('cart', {})
            pid_str = str(product_id)
            cart[pid_str] = cart.get(pid_str, 0) + quantity
            session['cart'] = cart

    @staticmethod
    def update_quantity(product_id, quantity, user=None):
        if quantity <= 0:
            CartService.remove_from_cart(product_id, user)
            return

        if user and user.is_authenticated:
            cart = Cart.query.filter_by(user_id=user.id).first()
            if cart:
                item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
                if item:
                    item.quantity = quantity
                    db.session.commit()
        else:
            cart = session.get('cart', {})
            pid_str = str(product_id)
            if pid_str in cart:
                cart[pid_str] = quantity
                session['cart'] = cart

    @staticmethod
    def remove_from_cart(product_id, user=None):
        if user and user.is_authenticated:
            cart = Cart.query.filter_by(user_id=user.id).first()
            if cart:
                item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
                if item:
                    db.session.delete(item)
                    db.session.commit()
        else:
            cart = session.get('cart', {})
            pid_str = str(product_id)
            if pid_str in cart:
                del cart[pid_str]
                session['cart'] = cart

    @staticmethod
    def sync_cart_on_login(user):
        """Merges session cart into user's database cart."""
        session_cart = session.pop('cart', None)
        if not session_cart:
            return

        cart = Cart.query.filter_by(user_id=user.id).first()
        if not cart:
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()

        for product_id, quantity in session_cart.items():
            item = CartItem.query.filter_by(cart_id=cart.id, product_id=int(product_id)).first()
            if item:
                item.quantity += quantity
            else:
                item = CartItem(cart_id=cart.id, product_id=int(product_id), quantity=quantity)
                db.session.add(item)
        db.session.commit()
