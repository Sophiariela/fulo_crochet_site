from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models.product import Product, Category
from app.models.order import Order
from app.models.user import User
from app.models.cms import Banner, Storytelling, PopupConfig
from app import db
from werkzeug.utils import secure_filename
import os
from functools import wraps

admin_bp = Blueprint('admin', __name__)
admin_bp.strict_slashes = False

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/', strict_slashes=False)
@login_required
@admin_required
def dashboard():
    stats = {
        'products': Product.query.count(),
        'orders': Order.query.count(),
        'users': User.query.filter_by(is_admin=False).count(),
        'categories': Category.query.count()
    }
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)

# PRODUCTS CRUD
@admin_bp.route('/products')
@login_required
@admin_required
def products():
    all_products = Product.query.all()
    return render_template('admin/products/index.html', products=all_products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def product_add():
    if request.method == 'POST':
        name = request.form.get('name')
        subtitle = request.form.get('subtitle')
        price = request.form.get('price')
        discount_price = request.form.get('discount_price')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        collection = request.form.get('collection')
        stock = request.form.get('stock')
        sizes = request.form.getlist("sizes")
        sizes_str = ",".join(sizes)
        is_featured = 'is_featured' in request.form
        is_accompanied = 'is_accompanied' in request.form
        technical_details = request.form.get('technical_details')
        shipping_and_returns = request.form.get('shipping_and_returns')
        
        image_urls = []
        for i in range(1, 5):
            file = request.files.get(f'image_{i}')
            if file and file.filename:
                filename = secure_filename(file.filename)
                img_path = os.path.join(current_app.root_path, 'static/images')
                if not os.path.exists(img_path): os.makedirs(img_path)
                file.save(os.path.join(img_path, filename))
                image_urls.append(f'/static/images/{filename}')
            else:
                image_urls.append(None)

        new_product = Product(
            name=name, 
            subtitle=subtitle,
            price=price, 
            discount_price=discount_price or None,
            description=description, 
            category_id=category_id, 
            collection=collection,
            stock=stock, 
            sizes=sizes_str,
            is_featured=is_featured,
            is_accompanied=is_accompanied,
            technical_details=technical_details,
            shipping_and_returns=shipping_and_returns,
            image_url=image_urls[0],
            image_url_2=image_urls[1],
            image_url_3=image_urls[2],
            image_url_4=image_urls[3]
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Produto adicionado!', 'success')
        return redirect(url_for('admin.products'))
    
    categories = Category.query.all()
    return render_template('admin/products/form.html', product=None, categories=categories)

@admin_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def product_edit(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.subtitle = request.form.get('subtitle')
        product.price = request.form.get('price')
        product.discount_price = request.form.get('discount_price') or None
        product.description = request.form.get('description')
        product.category_id = request.form.get('category_id')
        product.collection = request.form.get('collection')
        product.stock = request.form.get('stock')
        
        sizes = request.form.getlist("sizes")
        product.sizes = ",".join(sizes) if sizes else ""
        
        product.is_featured = 'is_featured' in request.form
        product.is_accompanied = 'is_accompanied' in request.form
        product.technical_details = request.form.get('technical_details') or ""
        product.shipping_and_returns = request.form.get('shipping_and_returns') or ""
        
        for i in range(1, 5):
            file = request.files.get(f'image_{i}')
            if file and file.filename:
                filename = secure_filename(file.filename)
                img_path = os.path.join(current_app.root_path, 'static/images')
                if not os.path.exists(img_path): os.makedirs(img_path)
                file.save(os.path.join(img_path, filename))
                url = f'/static/images/{filename}'
                if i == 1: product.image_url = url
                elif i == 2: product.image_url_2 = url
                elif i == 3: product.image_url_3 = url
                elif i == 4: product.image_url_4 = url
            
        db.session.commit()
        flash('Produto atualizado!', 'success')
        return redirect(url_for('admin.products'))
    
    categories = Category.query.all()
    return render_template('admin/products/form.html', product=product, categories=categories)

# CATEGORIES CRUD
@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    all_categories = Category.query.all()
    return render_template('admin/categories/index.html', categories=all_categories)

@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
@admin_required
def category_add():
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug') or name.lower().replace(' ', '-')
        description = request.form.get('description')
        
        new_cat = Category(name=name, slug=slug, description=description)
        db.session.add(new_cat)
        db.session.commit()
        flash('Categoria adicionada!', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/categories/form.html', category=None)

@admin_bp.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def category_edit(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.slug = request.form.get('slug') or category.name.lower().replace(' ', '-')
        category.description = request.form.get('description')
        db.session.commit()
        flash('Categoria atualizada!', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/categories/form.html', category=category)

@admin_bp.route('/categories/delete/<int:id>')
@login_required
@admin_required
def category_delete(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Categoria removida!', 'info')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/products/delete/<int:id>')
@login_required
@admin_required
def product_delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Produto removido!', 'info')
    return redirect(url_for('admin.products'))

# BANNERS CRUD
@admin_bp.route('/banners')
@login_required
@admin_required
def banners():
    all_banners = Banner.query.order_by(Banner.order.asc()).all()
    return render_template('admin/banners/index.html', banners=all_banners)

@admin_bp.route('/banners/add', methods=['GET', 'POST'])
@login_required
@admin_required
def banner_add():
    if request.method == 'POST':
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        description = request.form.get('description')
        button_text = request.form.get('button_text')
        link_url = request.form.get('link_url')
        order_val = request.form.get('order', '0')
        order = int(order_val) if order_val and order_val.isdigit() else 0
        is_active = 'is_active' in request.form
        
        file = request.files.get('image')
        mobile_file = request.files.get('mobile_image')
        
        image_url = None
        mobile_image_url = None
        
        img_path = os.path.join(current_app.root_path, 'static/images')
        if not os.path.exists(img_path): os.makedirs(img_path)

        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(img_path, filename))
            image_url = f'/static/images/{filename}'
            
        if mobile_file and mobile_file.filename:
            m_filename = "mobile_" + secure_filename(mobile_file.filename)
            mobile_file.save(os.path.join(img_path, m_filename))
            mobile_image_url = f'/static/images/{m_filename}'
            
        new_banner = Banner(
            title=title, 
            subtitle=subtitle, 
            description=description,
            button_text=button_text,
            image_url=image_url, 
            mobile_image_url=mobile_image_url,
            link_url=link_url,
            order=order,
            is_active=is_active
        )
        db.session.add(new_banner)
        db.session.commit()
        flash('Banner adicionado com sucesso!', 'success')
        return redirect(url_for('admin.banners'))
    return render_template('admin/banners/form.html', banner=None)

@admin_bp.route('/banners/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def banner_edit(id):
    banner = Banner.query.get_or_404(id)
    if request.method == 'POST':
        banner.title = request.form.get('title')
        banner.subtitle = request.form.get('subtitle')
        banner.description = request.form.get('description')
        banner.button_text = request.form.get('button_text')
        banner.link_url = request.form.get('link_url')
        order_val = request.form.get('order', '0')
        banner.order = int(order_val) if order_val and order_val.isdigit() else 0
        banner.is_active = 'is_active' in request.form
        
        file = request.files.get('image')
        mobile_file = request.files.get('mobile_image')
        
        img_path = os.path.join(current_app.root_path, 'static/images')
        if not os.path.exists(img_path): os.makedirs(img_path)

        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(img_path, filename))
            banner.image_url = f'/static/images/{filename}'
            
        if mobile_file and mobile_file.filename:
            m_filename = "mobile_" + secure_filename(mobile_file.filename)
            mobile_file.save(os.path.join(img_path, m_filename))
            banner.mobile_image_url = f'/static/images/{m_filename}'
            
        db.session.commit()
        flash('Banner atualizado com sucesso!', 'success')
        return redirect(url_for('admin.banners'))
    return render_template('admin/banners/form.html', banner=banner)

@admin_bp.route('/banners/delete/<int:id>')
@login_required
@admin_required
def banner_delete(id):
    banner = Banner.query.get_or_404(id)
    db.session.delete(banner)
    db.session.commit()
    flash('Banner removido!', 'info')
    return redirect(url_for('admin.banners'))

# STORYTELLING CRUD
@admin_bp.route('/storytelling')
@login_required
@admin_required
def storytelling():
    items = Storytelling.query.all()
    return render_template('admin/storytelling/index.html', items=items)

@admin_bp.route('/storytelling/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def storytelling_edit(id):
    item = Storytelling.query.get_or_404(id)
    if request.method == 'POST':
        item.title = request.form.get('title')
        item.subtitle = request.form.get('subtitle')
        item.content = request.form.get('content')
        item.button_text = request.form.get('button_text')
        item.button_link = request.form.get('button_link')
        item.layout_type = request.form.get('layout_type')
        
        file = request.files.get('image')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.root_path, 'static/images', filename))
            item.image_url = f'/static/images/{filename}'
            
        db.session.commit()
        flash('Conteúdo atualizado!', 'success')
        return redirect(url_for('admin.storytelling'))
    return render_template('admin/storytelling/form.html', item=item)

# POPUP MANAGEMENT
@admin_bp.route('/popup', methods=['GET', 'POST'])
@login_required
@admin_required
def popup_config():
    config = PopupConfig.query.first()
    if not config:
        config = PopupConfig()
        db.session.add(config)
        db.session.commit()
        
    if request.method == 'POST':
        config.title = request.form.get('title')
        config.subtitle = request.form.get('subtitle')
        config.discount_text = request.form.get('discount_text')
        config.button_text = request.form.get('button_text')
        config.is_active = 'is_active' in request.form
        config.delay_seconds = request.form.get('delay_seconds', 3)
        
        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            img_path = os.path.join(current_app.root_path, 'static/images')
            if not os.path.exists(img_path): os.makedirs(img_path)
            file.save(os.path.join(img_path, filename))
            config.image_url = f'/static/images/{filename}'
            
        db.session.commit()
        flash('Configuração do popup atualizada!', 'success')
        return redirect(url_for('admin.popup_config'))
        
    return render_template('admin/popup/form.html', config=config)

# ORDERS
@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders/index.html', orders=all_orders)

@admin_bp.route('/orders/<int:id>')
@login_required
@admin_required
def order_detail(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/orders/detail.html', order=order)

# CLIENTS
@admin_bp.route('/clients')
@login_required
@admin_required
def clients():
    all_users = User.query.all()
    return render_template('admin/clients/index.html', users=all_users)

@admin_bp.route('/clients/<int:id>/history')
@login_required
@admin_required
def client_history(id):
    user = User.query.get_or_404(id)
    from decimal import Decimal
    orders = Order.query.filter_by(user_id=id).order_by(Order.created_at.desc()).all()
    total_spent = sum((o.total_amount for o in orders), Decimal('0.00'))
    return render_template('admin/clients/history.html', user=user, orders=orders, total_spent=total_spent)
