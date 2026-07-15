from app import create_app, db
from app.models.product import Product, Category
from app.models.cms import Banner, Storytelling, PopupConfig
from app.models.user import User
from decimal import Decimal
import os

app = create_app()

def seed():
    with app.app_context():
        # Create tables
        db.drop_all() # Reset for a clean seed
        db.create_all()

        # Create Admin
        if not User.query.filter_by(email='admin@fulo.com.br').first():
            admin = User(name='Admin Fulô', email='admin@fulo.com.br', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            print("Admin criado: admin@fulo.com.br / admin123")

        # Categories
        cat_map = {
            'vestidos': 'Vestidos',
            'tops': 'Tops',
            'biquinis': 'Biquínis',
            'saias & shorts': 'Saias & Shorts',
            'conjuntos': 'Conjuntos',
            'acessorios': 'Acessórios'
        }
        categories = {}
        for slug, name in cat_map.items():
            cat = Category(name=name, slug=slug)
            db.session.add(cat)
            db.session.flush()
            categories[slug] = cat
        print("Categorias criadas.")

        # Banners
        banners = [
            Banner(
                title='Brasilidade em cada ponto',
                subtitle='COLEÇÃO VERÃO 2026',
                image_url='/static/images/banner-fulo.png',
                link_url='/shop?collection=Brasilidade',
                order=1
            ),
            Banner(
                title='O novo artesanal',
                subtitle='LANÇAMENTOS',
                image_url='/static/images/banner.png',
                link_url='/shop?collection=Lançamentos',
                order=2
            )
        ]
        db.session.add_all(banners)

        # Storytelling
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

        # Popup Config
        popup = PopupConfig(
            title='Ganhe 10% OFF',
            subtitle='BEM-VINDA À FULÔ',
            discount_text='USE O CUPOM: FULO10',
            button_text='QUERO MEU DESCONTO',
            is_active=True,
            delay_seconds=3,
            image_url='/static/images/conjunto-flor-de-maio-.png'
        )
        db.session.add(popup)

        # Products from legacy data
        products_data = [
            ("Vestido Bahia Blue", 200.00, "Vestido halter neck em crochê artesanal, linha 100% algodão azul royal vibrante.", "vestidos", "/static/images/vestido-croche-halter-azul-royal.jpg"),
            ("Conjunto Flor de Maio", 190.00, "Conjunto composto por top e saia mini em crochê artesanal, linha 100% algodão off-white.", "conjuntos", "/static/images/conjunto-croche-top-saia-offwhite-floral.png"),
            ("Vestido Nevoa", 300.00, "Vestido curto em crochê artesanal, linha 100% algodão off-white. Halter neck com costas abertas.", "vestidos", "/static/images/vestido-croche-halter-costas-abertas-offwhite.png"),
            ("Vestido Areia Dourada", 300.00, "Vestido assimétrico ombro único em crochê artesanal, linha 100% algodão off-white.", "vestidos", "/static/images/vestido-croche-ombro-unico-assimetrico-offwhite.png"),
            ("Top Terra Preta", 70.00, "Top triangular halter neck em crochê artesanal, 100% poliamida na cor chocolate.", "tops", "/static/images/top-croche-halter-chocolate-floral-micanga.png"),
            ("Top Orquidea", 90.00, "Top em crochê artesanal, linha 100% algodão off-white com aplicação de orquídea multicolorida.", "tops", "/static/images/top-croche-halter-offwhite-aplicacao-orquidea.png"),
            ("Saia Piteira", 100.00, "Saia mini em crochê artesanal, linha 100% algodão off-white. Cintura alta com cordão regulável.", "saias & shorts", "/static/images/saia-croche-mini-cintura-alta-offwhite.png"),
            ("Vestido Estrela do Mar", 270.00, "Vestido em crochê artesanal, linha 100% algodão branca com aplicações de estrelas-do-mar.", "vestidos", "/static/images/vestido-croche-alca-fina-branco-aplicacao.png"),
            ("Conjunto Noite Selvagem", 260.00, "Conjunto em crochê artesanal, linha 100% algodão cru com bordado de onça pintada.", "conjuntos", "/static/images/conjunto-croche-top-saia-midi-franja.png"),
            ("Conjunto Liana", 300.00, "Conjunto em crochê artesanal, linha 100% algodão bicolor com franjas douradas.", "conjuntos", "/static/images/conjunto-croche-bicolor-franja-dourada.jpg"),
            ("Vestido Acai", 250.00, "Vestido em crochê artesanal, linha 100% algodão na cor vinho. Alças finas, corte reto.", "vestidos", "/static/images/vestido-croche-alca-fina-vinho.png"),
            ("Vestido Jabuticaba", 280.00, "Vestido em crochê artesanal, linha 100% algodão vinho escuro. Alças finas com pingentes dourados.", "vestidos", "/static/images/vestido-croche-decote-v-vinho-babado.png"),
            ("Vestido Sol do Tapajos", 220.00, "Vestido em crochê artesanal, linha 100% algodão cru. Alças finas com pingentes dourados.", "vestidos", "/static/images/vestido-croche-rendado-algodao-cru.jpg"),
            ("Top Arara", 120.00, "Top tomara-que-caia em crochê artesanal with bordado de arara-azul em ponto tapeçaria.", "tops", "/static/images/top-croche-tomara-caia-bordado-arara.png"),
            ("Top Por do Amazonas", 50.00, "Top em crochê artesanal, linha 100% algodão laranja queimado. Modelo triângulo.", "tops", "/static/images/top-croche-triangulo-laranja-micanga.png"),
            ("Top Cacau", 50.00, "Top em crochê artesanal, linha 100% algodão marrom. Modelo triângulo with alças reguláveis.", "tops", "/static/images/top-croche-triangulo-marrom-rendado.png"),
            ("Top Cocada", 100.00, "Top colete em crochê artesanal, linha 100% algodão cru. Modelo halter with abertura frontal.", "tops", "/static/images/top-croche-colete-halter-algodao-cru.png"),
            ("Top Flor de Orquidea", 90.00, "Top em crochê artesanal, linha 100% algodão branco with aplicação de orquídea em relevo.", "tops", "/static/images/top-croche-halter-branco-aplicacao-floral.png"),
            ("Top Raiz Brasileira", 70.00, "Top em crochê artesanal, linha 100% algodão verde with detalhes nas cores do Brasil.", "tops", "/static/images/top-croche-cropped-verde-brasil.png"),
            ("Bolsa Buriti", 100.00, "Bolsa em crochê artesanal, linha 100% algodão marrom. Modelo meia-lua with alça em miçangas.", "acessorios", "/static/images/bolsa-croche-meia-lua-madeira-marrom.jpg"),
            ("Bandana Folha Amazonica", 70.00, "Bandana em crochê artesanal, linha 100% algodão verde. Formato aba larga with amarração.", "acessorios", "/static/images/bandana-croche-verde-algodao-artesanal.png"),
            ("Top Sereia Azul", 75.00, "Top triângulo em crochê artesanal, fio azul royal with aplicação de paetes circulares.", "tops", "/static/images/top-croche-triangulo-azul-paetes.png"),
            ("Top Ouro de Midas", 75.00, "Top triângulo em crochê artesanal with aplicação de paetes dourados. Efeito metálico exclusivo.", "tops", "/static/images/top-croche-triangulo-dourado-paetes.png"),
            ("Top Lua Cheia", 85.00, "Top triângulo assimétrico em crochê artesanal, algodão off white with argolas e moedas.", "tops", "/static/images/top-croche-triangulo-offwhite-argolas.png"),
            ("Top Ondas do Caribe", 85.00, "Top triângulo em crochê artesanal, fio azul. Modelagem assimétrica with trama aberta.", "tops", "/static/images/top-croche-triangulo-azul-assimetrico.png"),
            ("Top Noite Estrelada", 85.00, "Top triângulo em crochê artesanal, fio preto. Modelagem assimétrica with trama aberta.", "tops", "/static/images/top-croche-triangulo-preto-trama-aberta.png"),
            ("Top Galaxia Profunda", 85.00, "Top triângulo em crochê artesanal, fio preto. Modelagem assimétrica with alça única.", "tops", "/static/images/top-croche-triangulo-preto-alca-unica.png"),
            ("Biquini Rainha Negra", 120.00, "Conjunto biquíni em crochê artesanal, fio preto with miçangas e correntes douradas.", "biquinis", "/static/images/biquini-croche-preto-micanga-corrente.png"),
            ("Biquini Ceu de Verao", 120.00, "Conjunto biquíni em crochê artesanal, fio azul claro. Top triângulo with trama em ponto renda.", "biquinis", "/static/images/biquini-croche-triangulo-azul-rendado.png"),
            ("Biquini Nevoa de Prata", 120.00, "Conjunto biquíni em crochê artesanal, fio prata. Efeito metálico sutil e delicado.", "biquinis", "/static/images/biquini-croche-prata-metalico-micanga.png"),
            ("Biquini Ipanema Gold", 120.00, "Conjunto biquíni em crochê artesanal, listras preto e dourado with argolas douradas.", "biquinis", "/static/images/biquini-croche-preto-dourado-argola.png"),
            ("Conjunto Moca Baiana", 120.00, "Conjunto em crochê artesanal, fio multicolor. Top triângulo e sainha de cintura alta.", "conjuntos", "/static/images/conjunto-croche-top-saia-multicolor.png"),
            ("Conjunto Nevoa", 200.00, "Conjunto em crochê artesanal, algodão off white. Top with alça fina e sainha with franjas.", "conjuntos", "/static/images/conjunto-croche-top-saia-franja-offwhite.png"),
            ("Vestido Brasileirinha", 270.00, "Vestido tomara-que-caia em crochê artesanal, fio multicolor with listras horizontais.", "vestidos", "/static/images/vestido-croche-tomara-caia-multicolor.jpg"),
        ]

        for name, price, desc, cat_slug, img in products_data:
            product = Product(
                name=name,
                price=Decimal(str(price)),
                description=desc,
                category_id=categories[cat_slug].id,
                image_url=img,
                is_active=True,
                is_featured=True if "Vestido" in name or "Conjunto" in name else False,
                collection="Brasilidade" if price > 150 else "Lançamentos"
            )
            db.session.add(product)

        db.session.commit()
        print(f"Seed finalizado! {len(products_data)} produtos inseridos.")

if __name__ == '__main__':
    seed()
