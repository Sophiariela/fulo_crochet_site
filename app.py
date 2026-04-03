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
        "descricao": "Vestido em crochê artesanal, linha 100% algodão branca com aplicações de estrelas-do-mar coloridas (azul, rosa, dourado). Alças finas, barra com babado rosa em ponto leque. Cintura marcada, trama vazada. Forro opcional. Lavar à mão, secar à sombra..",
	"imagem": "/static/imagens/vestido-estrela-do-mar.png",
        "categoria": "vestidos"
    }
]

@app.route('/')
def index():
    return render_template('index.html', produtos=PRODUTOS)

if __name__ == '__main__':
    app.run(debug=True)

