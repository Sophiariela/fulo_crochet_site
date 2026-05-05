from app import create_app, db
from app.models.product import Product, Category
from app.models.cms import Banner, Storytelling
from app.models.user import User
from decimal import Decimal

app = create_app()

def seed():
    with app.app_context():
        # Create tables
        db.create_all()

        # Create Admin
        if not User.query.filter_by(email='admin@fulo.com.br').first():
            admin = User(name='Admin Fulô', email='admin@fulo.com.br', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            print("Admin criado: admin@fulo.com.br / admin123")

        # Categories
        cat_names = ['Vestidos', 'Tops', 'Biquínis', 'Saias', 'Conjuntos', 'Acessórios']
        categories = {}
        for name in cat_names:
            cat = Category.query.filter_by(name=name).first()
            if not cat:
                cat = Category(name=name, slug=name.lower().replace('í', 'i').replace('ú', 'u'))
                db.session.add(cat)
                db.session.flush()
            categories[name] = cat
        print("Categorias verificadas/criadas.")

        # Banners
        if not Banner.query.first():
            banners = [
                Banner(
                    title='Brasilidade em cada ponto',
                    subtitle='COLEÇÃO VERÃO 2026',
                    image_url='/static/images/banner-fulo.png',
                    link_url='/shop?collection=Brasilidade'
                ),
                Banner(
                    title='O novo artesanal',
                    subtitle='LANÇAMENTOS',
                    image_url='/static/images/banner.png',
                    link_url='/shop?collection=Lançamentos'
                )
            ]
            db.session.add_all(banners)
            print("Banners inseridos.")

        # Storytelling
        if not Storytelling.query.first():
            sections = [
                Storytelling(
                    section_name='brand_intro',
                    title='Mãos que tecem o amanhã.',
                    subtitle='NOSSA ESSÊNCIA',
                    content='A FULÔ nasceu do desejo de unir a tradição milenar do crochê ao design contemporâneo. Cada peça é única, feita com calma e dedicação por artesãs brasileiras.',
                    image_url='/static/images/vestido-croche-rendado-algodao-cru.jpg',
                    layout_type='image_left'
                ),
                Storytelling(
                    section_name='craftsmanship',
                    title='O tempo do feito à mão.',
                    subtitle='PROCESSO ARTESANAL',
                    content='Diferente da moda industrial, respeitamos o tempo das mãos. Uma peça FULÔ leva dias para ser concluída, garantindo qualidade e alma em cada ponto.',
                    image_url='/static/images/top-croche-colete-halter-algodao-cru.png',
                    layout_type='image_right'
                )
            ]
            db.session.add_all(sections)
            print("Storytelling inserido.")

        # Products (Sample)
        if not Product.query.first():
            products_data = [
                {
                    'name': 'Vestido Maré Azul',
                    'subtitle': 'Crochê Rendado',
                    'price': Decimal('589.00'),
                    'description': 'Vestido longo em crochê com trama aberta e detalhes em seda.',
                    'category': 'Vestidos',
                    'collection': 'Brasilidade',
                    'image_url': '/static/images/vestido-croche-halter-azul-royal.jpg',
                    'stock': 5,
                    'is_featured': True
                },
                {
                    'name': 'Top Aurora',
                    'subtitle': 'Aplicações Florais',
                    'price': Decimal('249.00'),
                    'description': 'Top halter com aplicações de flores feitas à mão.',
                    'category': 'Tops',
                    'collection': 'Lançamentos',
                    'image_url': '/static/images/top-croche-halter-branco-aplicacao-floral.png',
                    'stock': 10,
                    'is_featured': True
                },
                {
                    'name': 'Bolsa Meia Lua',
                    'subtitle': 'Acessório Atemporal',
                    'price': Decimal('320.00'),
                    'description': 'Bolsa em crochê com alça de madeira natural.',
                    'category': 'Acessórios',
                    'collection': 'Brasilidade',
                    'image_url': '/static/images/bolsa-croche-meia-lua-madeira-marrom.jpg',
                    'stock': 3,
                    'is_featured': True
                }
            ]
            for p_data in products_data:
                cat_name = p_data.pop('category')
                p_data['category_id'] = categories[cat_name].id
                product = Product(**p_data)
                db.session.add(product)
            print("Produtos de exemplo inseridos.")

        db.session.commit()
        print("Seed finalizado com sucesso!")

if __name__ == '__main__':
    seed()
