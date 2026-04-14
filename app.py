from flask import Flask, render_template

app = Flask(__name__)

PRODUTOS = [
    {
        "id": 1,
        "nome": "Vestido Bahia Blue",
        "preco": 200.00,
        "descricao": "Vestido halter neck em crochê artesanal, linha 100% algodão azul royal vibrante. Amarração no pescoço, cintura marcada, barra com babado em ponto pipoca. Comprimento mini, trama fechada. Forro opcional. Lavar à mão, secar à sombra.",
        "imagem": "/static/imagens/vestido-bahia-blue.jpg",
        "categoria": "vestidos"
    },
    {
        "id": 2,
        "nome": "Conjunto Flor de Maio",
        "preco": 190.00,
        "descricao": "Conjunto composto por top e saia mini em crochê artesanal, linha 100% algodão off-white com detalhes vinho/rosa/. Top com aplicação de orquídea e tiras reguláveis. Saia com cordão, miçangas vermelhas e babado. Disponível separadamente ou conjunto. Lavar à mão, secar à sombra.",
        "imagem": "/static/imagens/conjunto-flor-de-maio.png",
        "categoria": "conjuntos"
    },
    {
        "id": 3,
        "nome": "Vestido Nevoa",
        "preco": 300.00,
        "descricao": "Vestido curto em crochê artesanal, linha 100% algodão off-white. Halter neck com costas abertas, babado na barra. Trama aberta estilo beach/festival, comprimento mini. Forro opcional. Lavar à mão, secar à sombra.",
        "imagem": "/static/imagens/vestido-nevoa.png",
        "categoria": "vestidos"
    },
    {
        "id": 4,
        "nome": "Vestido Areia Dourada",
        "preco": 300.00,
        "descricao": "Vestido assimétrico ombro único em crochê artesanal, linha 100% algodão off-white. Alça larga com detalhe vazado lateral, faixa floral assimétrica. Comprimento médio, barra assimétrica. Trama aberta estilo beach. Forro opcional. Lavar à mão, secar à sombra.",
        "imagem": "/static/imagens/vestido-areia-dourada.png",
        "categoria": "vestidos"
    },
    {
        "id": 5,
        "nome": "Top Terra Preta",
        "preco": 70.00,
        "descricao": "Top triangular halter neck em crochê artesanal, 100% poliamida na cor chocolate/marrom. Amarração no pescoço e costas, aplicações florais com miçangas em tons terrosos. Tiras reguláveis com miçangas de madeira. Lavar à mão, secar à sombra.",
        "imagem": "/static/imagens/top-terra-preta.png",
        "categoria": "tops"
    },
    {

	"id": 6,
	"nome": "Top Orquídea",
	"preco": 90.00,
	"descricao": "Top em crochê artesanal, linha 100% algodão off-white com aplicação de orquídea multicolorida (vinho, rosa). Amarração no pescoço e costas, tiras reguláveis com miçangas. Trama aberta estilo beach/festival. Lavar à mão, secar à sombra.",
	"imagem": "/static/imagens/top-orquidea.png",
	"categoria": "tops"

   },
   {
	"id": 7,
	"nome": "Saia Piteira",
	"preco": 100.00,
	"descricao": "Saia mini em crochê artesanal, linha 100% algodão off-white. Cintura alta com cordão regulável e miçangas vermelhas, barra com babado em ponto leque. Elástico interno para melhor ajuste. Lavar à mão, secar à sombra.",
	"imagem": "/static/imagens/saia-piteira.png",
	"categoria": "saias & shorts"

    },
    {
        "id": 8,
        "nome": "Vestido Estrela do Mar",
        "preco": 270.00,
        "descricao": "Vestido em crochê artesanal, linha 100% algodão branca com aplicações de estrelas-do-mar coloridas (azul, rosa, dourado). Alças finas, barra com babado rosa em ponto leque. Cintura marcada, trama vazada. Forro opcional. Lavar à mão, secar à sombra.",
	"imagem": "/static/imagens/vestido-estrela-do-mar.png",
        "categoria": "vestidos"
    },
    {
        "id": 9,
        "nome": "Conjunto Noite Selvagem",
        "preco": 260.00,
        "descricao": "Conjunto em crochê artesanal, linha 100% algodão cru com bordado de onça pintada. Top tomara-que-caia com franjas pingentes na barra. Saia midi em ponto rendado escuro, acabamento em franjas longas. Cintura marcada, sobreposição estruturada. Forro opcional. Lavar à mão, secar à sombra.",
        "imagem": "/static/imagens/conjunto-noite-selvagem.png",
        "categoria": "conjuntos"
    },
    {

 	"id": 10,
        "nome": "Conjunto Liana",
        "preco": 300.00,
        "descricao": "Conjunto em crochê artesanal, linha 100% algodão bicolor — top marrom com decote em V e franjas douradas, saia bege em ponto canelado com franjas longas e cinto trançado. Silhueta fluida, acabamento assimétrico. Forro opcional. Lavar à mão, secar à sombra.",
        "imagem": "/static/imagens/conjunto-liana.jpg",
	"categoria": "conjuntos"
    },
    {
        "id": 11,
        "nome": "Vestido Açaí",
        "preco": 250.00,
	"descricao": "Vestido em crochê artesanal, linha 100% algodão na cor vinho. Alças finas, corte reto ajustado ao corpo, barra em ponto concha. Trama fechada, caimento liso. Forro opcional. Lavar à mão, secar à sombra.",
        "imagem": "/static/imagens/vestido-açai.png",
	"categoria": "vestidos"
    },
    {
        "id": 12,
        "nome": "Vestido Jabutuicaba",
        "preco": 280.00,
	"descricao": "Vestido em crochê artesanal, linha 100% algodão vinho escuro. Alças finas com pingentes dourados, decote em V, trama vazada no corpo. Barra com babado em ponto leque, volume leve. Forro opcional. Lavar à mão, secar à sombra.",
        "imagem": "/static/imagens/vestido-jabuticaba.png",
	"categoria": "vestidos"
    },
    {
	"id": 13,
	"nome": "Vestido Sol do Tapajós",
	"preco": 220.00,
	"descricao": "Vestido em crochê artesanal, linha 100% algodão cru. Alças finas com pingentes dourados, decote em V, trama rendada ao longo do corpo. Barra com babado assimétrico em ponto leque. Forro opcional. Lavar à mão, secar à sombra.",
	"imagem": "/static/imagens/vestido-sol-do-tapajos.jpg",
	"categoria": "vestidos"
    },
    {
	"id": 14,
	"nome": "Top Arara",
	"preco": 120.00,
	"descricao": "Top tomara-que-caia em crochê artesanal, linha 100% algodão cru com bordado de arara-azul em ponto tapeçaria — azul, amarelo e verde. Estrutura tubular, barra reta. Peça única. Lavar à mão, secar à sombra.",
	"imagem": "/static/imagens/top-arara.png",
	"categoria": "tops"
    },
    {
	"id": 15,
	"nome": "Top Pôr do Amazônas",
	"preco": 50.00,
	"descricao": "Top em crochê artesanal, linha 100% algodão laranja queimado. Modelo triângulo com alças reguláveis, acabamento em ponto rendado nas bordas e pingentes em miçanga dourada. Ajuste por amarração. Lavar à mão, secar à sombra.",
	"imagem": "/static/imagens/top-por-do-amazonas.png",
	"categoria": "tops"
    },
    {
   	"id": 16, 
	"nome": "Top Cacau",
	"preco": 50.00,
	"descricao": "Top em crochê artesanal, linha 100% algodão marrom. Modelo triângulo com alças reguláveis em tiras, acabamento em ponto rendado na borda. Ajuste por amarração frontal e nas costas. Lavar à mão, secar à sombra.",
	"imagem": "/static/imagens/top-cacau.png",
	"categoria": "tops"
    },
    {
  	"id": 17,
	"nome": "Top Cocada",
	"preco": 100.00,
	"descricao": "Top colete em crochê artesanal, linha 100% algodão cru. Modelo halter com abertura frontal e pingente em miçanga dourada. Trama semi-aberta, caimento leve. Ajuste por amarração no pescoço. Lavar à mão, secar à sombra.",
	"imagem": "/static/imagens/top-cocada.png",
	"categoria": "tops"
    },
    {
	"id": 18,
	"nome": "Top Flor de Orquídea",
	"preco": 90.00,
	"descricao": "Top em crochê artesanal, linha 100% algodão branco com aplicação de orquídea em relevo e acabamento em miçangas pretas. Modelo halter com alça de contas, decote amplo. Peça única. Lavar à mão, secar à sombra.",
	"imagem": "/static/imagens/top-flor-de-orquidea.png",
	"categoria": "tops"
    },
    {
	"id": 19,
	"nome": "Top Raíz Brasileira",
	"preco": 70.00,
	"descricao": "Top em crochê artesanal, linha 100% algodão verde com detalhes nas cores da bandeira brasileira na barra. Modelo cropped com recorte geométrico frontal. Alça única regulável. Lavar à mão, secar à sombra.",
	"imagem": "/static/imagens/top-raiz-brasileira.png",
	"categoria": "tops"
    },
    {
	"id": 20,
	"nome": "Bolsa Buriti",
	"preco": 100.00,
	"descricao": "Bolsa em crochê artesanal, linha 100% algodão marrom. Modelo meia-lua com alça rígida em miçangas de madeira laranja. Trama fechada estruturada, abertura superior sem fechamento. Tamanho: médio. Lavar à mão, secar à sombra.",
	"imagem": "/static/imagens/bolsa-buriti.jpg",
	"categoria": "acessorios"
    },
    {
	"id": 21,
	"nome": "Bandana Folha Amazonica",
	"preco": 70.00,
	"descricao": "Bandana em crochê artesanal, linha 100% algodão verde. Formato aba larga com amarração em cordão fino. Trama semi-aberta, leve e ventilada. Ajuste por amarração. Lavar à mão, secar à sombra.",
	"imagem": "static/imagens/bandana-folha-amazonica.png",
	"categoria": "acessorios"
 }
]

@app.route('/')
def index():
    return render_template('index.html', produtos=PRODUTOS)

if __name__ == '__main__':
    app.run(debug=True)

