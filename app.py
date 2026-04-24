from flask import Flask, render_template

app = Flask(__name__)

PRODUTOS = [
    {
        "id": 1,
        "nome": "Vestido Bahia Blue",
        "preco": 200.00,
        "descricao": "Vestido halter neck em crochê artesanal, linha 100% algodão azul royal vibrante. Amarração no pescoço, cintura marcada, barra com babado em ponto pipoca. Comprimento mini, trama fechada. Forro opcional.",
        "imagem": "/static/imagens/vestido-bahia-blue.jpg",
        "categoria": "vestidos"
    },
    {
        "id": 2,
        "nome": "Conjunto Flor de Maio",
        "preco": 190.00,
        "descricao": "Conjunto composto por top e saia mini em crochê artesanal, linha 100% algodão off-white com detalhes vinho/rosa/. Top com aplicação de orquídea e tiras reguláveis. Saia com cordão, miçangas vermelhas e babado. Disponível separadamente ou conjunto.",
        "imagem": "/static/imagens/conjunto-flor-de-maio.png",
        "categoria": "conjuntos"
    },
    {
        "id": 3,
        "nome": "Vestido Nevoa",
        "preco": 300.00,
        "descricao": "Vestido curto em crochê artesanal, linha 100% algodão off-white. Halter neck com costas abertas, babado na barra. Trama aberta estilo beach/festival, comprimento mini. Forro opcional.",
        "imagem": "/static/imagens/vestido-nevoa.png",
        "categoria": "vestidos"
    },
    {
        "id": 4,
        "nome": "Vestido Areia Dourada",
        "preco": 300.00,
        "descricao": "Vestido assimétrico ombro único em crochê artesanal, linha 100% algodão off-white. Alça larga com detalhe vazado lateral, faixa floral assimétrica. Comprimento médio, barra assimétrica. Trama aberta estilo beach. Forro opcional.",
        "imagem": "/static/imagens/vestido-areia-dourada.png",
        "categoria": "vestidos"
    },
    {
        "id": 5,
        "nome": "Top Terra Preta",
        "preco": 70.00,
        "descricao": "Top triangular halter neck em crochê artesanal, 100% poliamida na cor chocolate/marrom. Amarração no pescoço e costas, aplicações florais com miçangas em tons terrosos. Tiras reguláveis com miçangas de madeira.",
        "imagem": "/static/imagens/top-terra-preta.png",
        "categoria": "tops"
    },
    {

	"id": 6,
	"nome": "Top Orquídea",
	"preco": 90.00,
	"descricao": "Top em crochê artesanal, linha 100% algodão off-white com aplicação de orquídea multicolorida (vinho, rosa). Amarração no pescoço e costas, tiras reguláveis com miçangas. Trama aberta estilo beach/festival.",
	"imagem": "/static/imagens/top-orquidea.png",
	"categoria": "tops"

   },
   {
	"id": 7,
	"nome": "Saia Piteira",
	"preco": 100.00,
	"descricao": "Saia mini em crochê artesanal, linha 100% algodão off-white. Cintura alta com cordão regulável e miçangas vermelhas, barra com babado em ponto leque. Elástico interno para melhor ajuste.",
	"imagem": "/static/imagens/saia-piteira.png",
	"categoria": "saias & shorts"

    },
    {
        "id": 8,
        "nome": "Vestido Estrela do Mar",
        "preco": 270.00,
        "descricao": "Vestido em crochê artesanal, linha 100% algodão branca com aplicações de estrelas-do-mar coloridas (azul, rosa, dourado). Alças finas, barra com babado rosa em ponto leque. Cintura marcada, trama vazada. Forro opcional.",
	"imagem": "/static/imagens/vestido-estrela-do-mar.png",
        "categoria": "vestidos"
    },
    {
        "id": 9,
        "nome": "Conjunto Noite Selvagem",
        "preco": 260.00,
        "descricao": "Conjunto em crochê artesanal, linha 100% algodão cru com bordado de onça pintada. Top tomara-que-caia com franjas pingentes na barra. Saia midi em ponto rendado escuro, acabamento em franjas longas. Cintura marcada, sobreposição estruturada.",
        "imagem": "/static/imagens/conjunto-noite-selvagem.png",
        "categoria": "conjuntos"
    },
    {

 	"id": 10,
        "nome": "Conjunto Liana",
        "preco": 300.00,
        "descricao": "Conjunto em crochê artesanal, linha 100% algodão bicolor — top marrom com decote em V e franjas douradas, saia bege em ponto canelado com franjas longas e cinto trançado. Silhueta fluida, acabamento assimétrico. Forro opcional.",
        "imagem": "/static/imagens/conjunto-liana.jpg",
	"categoria": "conjuntos"
    },
    {
        "id": 11,
        "nome": "Vestido Açaí",
        "preco": 250.00,
	"descricao": "Vestido em crochê artesanal, linha 100% algodão na cor vinho. Alças finas, corte reto ajustado ao corpo, barra em ponto concha. Trama fechada, caimento liso. Forro opcional.",
        "imagem": "/static/imagens/vestido-açai.png",
	"categoria": "vestidos"
    },
    {
        "id": 12,
        "nome": "Vestido Jabutuicaba",
        "preco": 280.00,
	"descricao": "Vestido em crochê artesanal, linha 100% algodão vinho escuro. Alças finas com pingentes dourados, decote em V, trama vazada no corpo. Barra com babado em ponto leque, volume leve. Forro opcional.",
        "imagem": "/static/imagens/vestido-jabuticaba.png",
	"categoria": "vestidos"
    },
    {
	"id": 13,
	"nome": "Vestido Sol do Tapajós",
	"preco": 220.00,
	"descricao": "Vestido em crochê artesanal, linha 100% algodão cru. Alças finas com pingentes dourados, decote em V, trama rendada ao longo do corpo. Barra com babado assimétrico em ponto leque. Forro opcional.",
	"imagem": "/static/imagens/vestido-sol-do-tapajos.jpg",
	"categoria": "vestidos"
    },
    {
	"id": 14,
	"nome": "Top Arara",
	"preco": 120.00,
	"descricao": "Top tomara-que-caia em crochê artesanal, linha 100% algodão cru com bordado de arara-azul em ponto tapeçaria — azul, amarelo e verde. Estrutura tubular, barra reta. Peça única.",
	"imagem": "/static/imagens/top-arara.png",
	"categoria": "tops"
    },
    {
	"id": 15,
	"nome": "Top Pôr do Amazônas",
	"preco": 50.00,
	"descricao": "Top em crochê artesanal, linha 100% algodão laranja queimado. Modelo triângulo com alças reguláveis, acabamento em ponto rendado nas bordas e pingentes em miçanga dourada. Ajuste por amarração.",
	"imagem": "/static/imagens/top-por-do-amazonas.png",
	"categoria": "tops"
    },
    {
   	"id": 16, 
	"nome": "Top Cacau",
	"preco": 50.00,
	"descricao": "Top em crochê artesanal, linha 100% algodão marrom. Modelo triângulo com alças reguláveis em tiras, acabamento em ponto rendado na borda. Ajuste por amarração frontal e nas costas.",
	"imagem": "/static/imagens/top-cacau.png",
	"categoria": "tops"
    },
    {
  	"id": 17,
	"nome": "Top Cocada",
	"preco": 100.00,
	"descricao": "Top colete em crochê artesanal, linha 100% algodão cru. Modelo halter com abertura frontal e pingente em miçanga dourada. Trama semi-aberta, caimento leve.",
	"imagem": "/static/imagens/top-cocada.png",
	"categoria": "tops"
    },
    {
	"id": 18,
	"nome": "Top Flor de Orquídea",
	"preco": 90.00,
	"descricao": "Top em crochê artesanal, linha 100% algodão branco com aplicação de orquídea em relevo e acabamento em miçangas pretas. Modelo halter com alça de contas, decote amplo.",
	"imagem": "/static/imagens/top-flor-de-orquidea.png",
	"categoria": "tops"
    },
    {
	"id": 19,
	"nome": "Top Raíz Brasileira",
	"preco": 70.00,
	"descricao": "Top em crochê artesanal, linha 100% algodão verde com detalhes nas cores da bandeira brasileira na barra. Modelo cropped com recorte geométrico frontal. Alça única regulável.",
	"imagem": "/static/imagens/top-raiz-brasileira.png",
	"categoria": "tops"
    },
    {
	"id": 20,
	"nome": "Bolsa Buriti",
	"preco": 100.00,
	"descricao": "Bolsa em crochê artesanal, linha 100% algodão marrom. Modelo meia-lua com alça rígida em miçangas de madeira laranja. Trama fechada estruturada, abertura superior.",
	"imagem": "/static/imagens/bolsa-buriti.jpg",
	"categoria": "acessorios"
    },
    {
	"id": 21,
	"nome": "Bandana Folha Amazonica",
	"preco": 70.00,
	"descricao": "Bandana em crochê artesanal, linha 100% algodão verde. Formato aba larga com amarração em cordão fino. Trama semi-aberta, leve e ventilada. Ajuste por amarração.",
	"imagem": "static/imagens/bandana-folha-amazonica.png",
	"categoria": "acessorios"
    },
    {
        "id": 22,
        "nome": "Top Sereia Azul",
        "preco": 75.00,
	"descricao": "Top triângulo em crochê artesanal, fio de polipropileno azul royal com aplicação de paetês circulares. Amarração frontal ajustável com pingentes nas pontas. Efeito escama que valoriza o decote.",
        "imagem": "/static/imagens/top-sereia-azul.png",
        "categoria": "tops"
    },
    {
        "id": 23,
        "nome": "Top Ouro de Midas",
        "preco": 75.00,
	"descricao": "Top triângulo em crochê artesanal, fio de polipropileno com aplicação de paetês dourados. Amarração frontal ajustável, acabamento com pingentes nas pontas. Efeito metálico exclusivo.",
        "imagem": "/static/imagens/top-ouro-de-midas.pgn",
        "categoria": "tops"
    },
    {
        "id": 24,
        "nome": "Top Lua Cheia",
        "preco": 85.00,
	"descricao": "Top triângulo assimétrico em crochê artesanal, linha 100% algodão off white. Aplicação de argolas e moedas que acompanham o movimento do corpo. Amarração ajustável no pescoço.",
        "imagem": "/static/imagens/top-lua-cheia.png",
        "categoria": "tops"
    },
    {
        "id": 25,
        "nome": "Top Ondas do Caribe",
        "preco": 85.00,
	"descricao": "Top triângulo em crochê artesanal, fio de polipropileno azul. Modelagem assimétrica com trama aberta e alça única ajustável.",
        "imagem": "/static/imagens/top-ondas-do-caribe.png",
        "categoria": "tops"
    },
    {
        "id": 26,
        "nome": "Top Noite Estrelada",
        "preco": 85.00,
	"descricao": "Top triângulo em crochê artesanal, fio de polipropileno preto. Modelagem assimétrica com trama aberta e alça única ajustável.",
        "imagem": "/static/imagens/top-noite-estrelada.png",
        "categoria": "tops"
    },
    {
        "id": 27,
        "nome": "Top Galaxia Profunda",
        "preco": 85.00,
	"descricao": "Top triângulo em crochê artesanal, fio de polipropileno preto. Modelagem assimétrica com trama aberta e alça única ajustável.",
        "imagem": "/static/imagens/top-galaxia-profunda.png",
        "categoria": "tops"
    },
    {
        "id": 28,
        "nome": "Biquini Rainha Negra",
        "preco": 120.00,
	"descricao": "Conjunto biquíni em crochê artesanal, fio de polipropileno preto. Top bandeau com aplicação de miçangas e calcinha com correntes douradas ajustáveis.",
        "imagem": "/static/imagens/biquini-rainha-negra.png",
        "categoria": "biquinis"
    },
    {
        "id": 29,
        "nome": "Biquini Céu de Verão",
        "preco": 120.00,
	"descricao": "Conjunto biquíni em crochê artesanal, fio de polipropileno azul claro. Top triângulo com amarração no pescoço e nas costas, calcinha com amarração lateral. Trama delicada em ponto renda",
        "imagem": "/static/imagens/biquini-ceu-de-verao.png",
        "categoria": "biquinis"
    },
    {
	"id": 30,
        "nome": "Biquini Nevoa de Prata",
        "preco": 120.00,
	"descricao": "Conjunto biquíni em crochê artesanal, fio de polipropileno prata. Top triângulo com acabamento em miçangas, calcinha com amarração lateral. Efeito metálico sutil e delicado.",
        "imagem": "/static/imagens/biquini-nevoa-de-prata.png",
        "categoria": "biquinis"
    },
    {
        "id": 31,
        "nome": "Biquini Ipanema Gold",
        "preco": 120.00,
	"descricao": "Conjunto biquíni em crochê artesanal, fio de polipropileno com listras preto e dourado. Top triângulo com argolas douradas centrais e calcinha de amarração lateral.",
        "imagem": "/static/imagens/biquini-ipanema-gold.png",
        "categoria": "biquinis"
    },
    {
        "id": 32,
        "nome": "Conjunto Moça Baiana",
        "preco": 120.00,
	"descricao": "Conjunto em crochê artesanal, fio de polipropileno multicolor. Top triângulo com amarração ajustável e sainha de cintura alta com listras vibrantes.",
        "imagem": "/static/imagens/conjunto-moca-baiana.png",
        "categoria": "conjuntos"
    },
    {
	"id": 33,
        "nome": "Conjunto Nevoa",
        "preco": 200.00,
	"descricao": "Conjunto em crochê artesanal, linha 100% algodão off white. Top com alça fina e amarração ajustável, sainha com cós elástico e barra com franjas. Trama aberta com volume leve e toque natural.",
        "imagem": "/static/imagens/conjunto-nevoa.png",
        "categoria": "conjuntos"
    },
    {
        "id": 34,
        "nome": "Vestido Brasileirinha",
        "preco": 270.00,
	"descricao": "Vestido tomara-que-caia em crochê artesanal, fio de polipropileno multicolor com listras horizontais em amarelo, verde, azul e laranja. Modelagem tubinho com barra reta e caimento leve. Cor e movimento em cada detalhe.",
        "imagem": "/static/imagens/vestido-brasileirinha.jpg",
        "categoria": "vestidos"
 }
]

@app.route('/')
def index():
    return render_template('index.html', produtos=PRODUTOS)

if __name__ == '__main__':
    app.run(debug=True)

