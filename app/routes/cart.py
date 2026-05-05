from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from app.services.cart_service import CartService

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/')
def index():
    items, total = CartService.get_cart_data(current_user)
    return render_template('public/cart.html', items=items, total=total)

@cart_bp.route('/json')
def get_cart_json():
    items, total = CartService.get_cart_data(current_user)
    items_json = []
    for item in items:
        items_json.append({
            'product_id': item['product_id'],
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image_url': item['image_url'],
            'subtotal': item['subtotal']
        })
    return jsonify({
        'items': items_json,
        'total': float(total),
        'count': sum(item['quantity'] for item in items)
    })

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add(product_id):
    quantity = int(request.form.get('quantity', 1))
    CartService.add_to_cart(product_id, quantity, current_user)
    flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('cart.index'))

@cart_bp.route('/update/<int:product_id>', methods=['POST'])
def update(product_id):
    quantity = int(request.form.get('quantity', 1))
    CartService.update_quantity(product_id, quantity, current_user)
    return redirect(url_for('cart.index'))

@cart_bp.route('/remove/<int:product_id>')
def remove(product_id):
    CartService.remove_from_cart(product_id, current_user)
    flash('Produto removido do carrinho.', 'info')
    return redirect(url_for('cart.index'))
