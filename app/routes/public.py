from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.models.product import Product, Category
from app.models.cms import Banner, Storytelling, NewsletterSubscriber
from app import db
from decimal import Decimal

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def home():
    banners = Banner.query.filter_by(is_active=True).order_by(Banner.order).all() or []
    featured_products = Product.query.filter_by(is_active=True, is_featured=True).limit(8).all() or []
    storytelling_sections = Storytelling.query.filter_by(is_visible=True).all() or []
    
    # Categorize products for specialized sections like "Lançamentos"
    new_arrivals = Product.query.filter_by(is_active=True, collection="Lançamentos").limit(4).all()
    brasilidade_collection = Product.query.filter_by(is_active=True, collection="Brasilidade").limit(4).all()

    return render_template(
        "public/index.html",
        banners=banners,
        featured_products=featured_products,
        storytelling_sections={s.section_name: s for s in storytelling_sections},
        new_arrivals=new_arrivals,
        brasilidade_collection=brasilidade_collection
    )

@public_bp.route("/shop")
def shop():
    category_slug = request.args.get('category')
    collection = request.args.get('collection')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_slug:
        query = query.join(Category).filter(Category.slug == category_slug)
    
    if collection:
        query = query.filter_by(collection=collection)
        
    produtos = query.all()
    categories = Category.query.all()
    collections = db.session.query(Product.collection).distinct().all()
    
    return render_template(
        "public/shop.html", 
        produtos=produtos, 
        categories=categories,
        collections=[c[0] for c in collections if c[0]]
    )

@public_bp.route("/collections")
def collections():
    categories = Category.query.all()
    collections_data = []
    for cat in categories:
        products = Product.query.filter_by(category_id=cat.id, is_active=True).limit(4).all()
        if products:
            collections_data.append({
                'name': cat.name,
                'slug': cat.slug,
                'products': products
            })
                
    return render_template("public/collections.html", collections=collections_data)

@public_bp.route("/product/<int:id>")
def product_detail(id):
    product = Product.query.get_or_404(id)
    related_products = Product.query.filter(Product.category_id == product.category_id, Product.id != product.id).limit(4).all()
    return render_template("public/product_detail.html", product=product, related_products=related_products)

@public_bp.route("/newsletter", methods=['POST'])
def newsletter_signup():
    email = request.form.get('email')
    if email:
        existing = NewsletterSubscriber.query.filter_by(email=email).first()
        if not existing:
            new_sub = NewsletterSubscriber(email=email)
            db.session.add(new_sub)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Obrigado por se inscrever!'})
    return jsonify({'status': 'error', 'message': 'E-mail inválido ou já cadastrado.'})

@public_bp.route("/search")
def search():
    query_text = request.args.get('q', '')
    if query_text:
        results = Product.query.join(Category, isouter=True).filter(
            (Product.name.ilike(f'%{query_text}%')) | 
            (Product.description.ilike(f'%{query_text}%')) |
            (Category.name.ilike(f'%{query_text}%')) |
            (Product.collection.ilike(f'%{query_text}%'))
        ).filter(Product.is_active == True).all()
    else:
        results = []
        
    categories = Category.query.all()
    collections = db.session.query(Product.collection).distinct().all()
    
    return render_template(
        "public/shop.html", 
        produtos=results, 
        search_query=query_text,
        categories=categories,
        collections=[c[0] for c in collections if c[0]]
    )

@public_bp.route("/termos-de-uso")
def termos_de_uso():
    return render_template("public/page.html", title="Termos de Uso", content="""
        <div class='content-section' style='line-height: 1.8; color: var(--muted);'>
            <p style='margin-bottom: 20px;'>Ao acessar este website, o usuário concorda com os presentes Termos de Uso.</p>
            <p style='margin-bottom: 20px;'>Os serviços, produtos e conteúdos disponibilizados neste site destinam-se exclusivamente a fins informativos e comerciais relacionados à marca.</p>
            <p style='margin-bottom: 20px;'>O usuário compromete-se a utilizar o website de forma lícita, respeitando todas as legislações aplicáveis.</p>
            <p style='margin-bottom: 20px;'>É proibida a reprodução, cópia, distribuição ou utilização indevida dos conteúdos disponibilizados sem autorização prévia.</p>
            <p style='margin-bottom: 20px;'>A empresa poderá atualizar estes Termos de Uso a qualquer momento, sem aviso prévio.</p>
            <p style='margin-bottom: 20px;'>Em caso de dúvidas, o usuário poderá entrar em contato pelos canais oficiais disponibilizados neste website.</p>
            <p style='margin-top: 40px; font-size: 0.9rem;'>Última atualização: Julho de 2026.</p>
        </div>
    """)

@public_bp.route("/politica-de-privacidade")
def privacy_policy():
    return render_template("public/page.html", title="Política de Privacidade", content="""
        <div class='content-section' style='line-height: 1.8; color: var(--muted);'>
            <p style='margin-bottom: 20px;'>A sua privacidade é importante para nós. É política da FULÔ respeitar a sua privacidade em relação a qualquer informação sua que possamos coletar no site FULÔ, e outros sites que possuímos e operamos.</p>
            <p style='margin-bottom: 20px;'>Solicitamos informações pessoais apenas quando realmente precisamos delas para lhe fornecer um serviço. Fazemo-lo por meios justos e legais, com o seu conhecimento e consentimento. Também informamos por que estamos coletando e como será usado.</p>
            <p style='margin-bottom: 20px;'>Apenas retemos as informações coletadas pelo tempo necessário para fornecer o serviço solicitado. Quando armazenamos dados, protegemos dentro de meios comercialmente aceitáveis para evitar perdas e roubos, bem como acesso, divulgação, cópia, uso ou modificação não autorizados.</p>
            <p style='margin-bottom: 20px;'>Não compartilhamos informações de identificação pessoal publicamente ou com terceiros, exceto quando exigido por lei.</p>
        </div>
    """)

@public_bp.route("/faq")
def faq():
    return render_template("public/page.html", title="Perguntas Frequentes", content="""
        <div class='faq-container'>
            <div class='faq-item' style='margin-bottom: 30px;'>
                <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem; margin-bottom: 10px;'>Quais as formas de pagamento?</h3>
                <p style='color: var(--muted);'>Aceitamos cartões de crédito (Visa, Mastercard, American Express, Elo) com parcelamento em até 6x sem juros, PIX com 5% de desconto e boleto bancário.</p>
            </div>
            <div class='faq-item' style='margin-bottom: 30px;'>
                <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem; margin-bottom: 10px;'>Qual o prazo de produção?</h3>
                <p style='color: var(--muted);'>Por ser um trabalho 100% artesanal, cada peça é iniciada após a confirmação do pedido. O prazo médio de produção varia de 7 a 15 dias úteis, dependendo da complexidade da peça.</p>
            </div>
            <div class='faq-item' style='margin-bottom: 30px;'>
                <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem; margin-bottom: 10px;'>Como cuidar da minha peça de crochê?</h3>
                <p style='color: var(--muted);'>Para garantir a longevidade da sua FULÔ: lave à mão com sabão neutro, não torça, retire o excesso de água com uma toalha e seque sempre à sombra em superfície plana. Nunca pendure sua peça úmida.</p>
            </div>
            <div class='faq-item' style='margin-bottom: 30px;'>
                <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem; margin-bottom: 10px;'>Vocês fazem peças sob medida?</h3>
                <p style='color: var(--muted);'>Sim! Adoramos criar peças personalizadas. Entre em contato através do nosso WhatsApp para conversarmos sobre o seu modelo e medidas específicas.</p>
            </div>
        </div>
    """)

@public_bp.route("/envios")
def envios():
    return render_template("public/page.html", title="Envios & Prazos", content="""
        <div class='content-section' style='line-height: 1.8; color: var(--muted);'>
            <p style='margin-bottom: 20px;'>Na FULÔ, valorizamos o tempo do fazer manual. Nossos prazos refletem o cuidado dedicado a cada ponto.</p>
            
            <h4 style='color: var(--text); margin-top: 30px; margin-bottom: 10px;'>Prazos de Entrega</h4>
            <p>O prazo total para você receber sua peça é a soma de: <br>
            <strong>Prazo de Produção (7 a 15 dias úteis) + Prazo da Transportadora (conforme seu CEP).</strong></p>
            
            <h4 style='color: var(--text); margin-top: 30px; margin-bottom: 10px;'>Modalidades de Envio</h4>
            <p>Utilizamos os Correios (PAC e SEDEX) e transportadoras privadas para garantir que sua peça chegue com segurança. O valor do frete é calculado automaticamente no checkout.</p>
            
            <h4 style='color: var(--text); margin-top: 30px; margin-bottom: 10px;'>Frete Grátis</h4>
            <p>Oferecemos frete grátis para todo o Brasil em compras acima de R$ 400,00.</p>
            
            <h4 style='color: var(--text); margin-top: 30px; margin-bottom: 10px;'>Rastreamento</h4>
            <p>Assim que sua peça for postada, você receberá um e-mail com o código de rastreio para acompanhar cada etapa do caminho até sua casa.</p>
        </div>
    """)

@public_bp.route("/trocas")
def trocas():
    return render_template("public/page.html", title="Trocas & Devoluções", content="""
        <div class='content-section' style='line-height: 1.8; color: var(--muted);'>
            <p style='margin-bottom: 20px;'>Queremos que você se sinta maravilhosa com sua FULÔ. Se algo não estiver como esperado, estamos aqui para resolver.</p>
            
            <h4 style='color: var(--text); margin-top: 30px; margin-bottom: 10px;'>Política de Troca</h4>
            <p>Você pode solicitar a troca em até 7 dias corridos após o recebimento. A primeira troca é por nossa conta (o frete de retorno e reenvio).</p>
            
            <h4 style='color: var(--text); margin-top: 30px; margin-bottom: 10px;'>Devoluções</h4>
            <p>Caso deseje desistir da compra, você tem o prazo de 7 dias corridos para solicitar o estorno total do valor pago.</p>
            
            <h4 style='color: var(--text); margin-top: 30px; margin-bottom: 10px;'>Condições da Peça</h4>
            <p>Para que a troca ou devolução seja aceita, a peça deve estar:</p>
            <ul style='margin-left: 20px; list-style-type: disc;'>
                <li>Com a etiqueta original fixada;</li>
                <li>Sem sinais de uso, lavagem ou odores;</li>
                <li>Na embalagem original ou similar que proteja o produto.</li>
            </ul>
            
            <h4 style='color: var(--text); margin-top: 30px; margin-bottom: 10px;'>Como solicitar?</h4>
            <p>Envie uma mensagem para o nosso e-mail <strong><a href='mailto:bastosjeniffer46@gmail.com' style='color: var(--accent);'>bastosjeniffer46@gmail.com</a></strong> ou telefone <strong><a href='tel:+5571986946669' style='color: var(--accent);'>+55 71 98694-6669</a></strong> com o número do seu pedido e o motivo da solicitação.</p>
        </div>
    """)

@public_bp.route("/contato")
def contato():
    return render_template("public/page.html", title="Fale Conosco", content="""
        <p>Estamos à disposição para tirar suas dúvidas e ouvir suas sugestões.</p>
    """)

@public_bp.route("/shipping/<zip_code>")
def get_shipping(zip_code):
    from app.services.checkout_service import CheckoutService
    from app.services.cart_service import CartService
    from flask_login import current_user
    
    subtotal = request.args.get('subtotal')
    if subtotal:
        try:
            subtotal = Decimal(subtotal)
        except:
            subtotal = Decimal('0.00')
    elif current_user.is_authenticated:
        _, subtotal = CartService.get_cart_data(current_user)
    else:
        subtotal = Decimal('0.00')
        
    res = CheckoutService.calculate_shipping(zip_code, subtotal)
    
    # Format decimals for JSON
    res['cost'] = float(res['cost'])
    return jsonify(res)

@public_bp.route("/storytelling")
def storytelling():
    sections = Storytelling.query.filter_by(is_visible=True).order_by(Storytelling.id).all()
    return render_template("public/storytelling.html", sections=sections)
