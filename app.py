from flask import Flask, render_template

app = Flask(__name__)

PRODUTOS = [
    {
        "id": 1,
        "nome": "Vestido Bahia Blue",
        "preco": 90.00,
        "descricao": "Para quem quer chegar e já ser o centro das atenções. O Bahia Blue é feito à mão em crochê com fio azul royal vibrante, silhueta halter neck que valoriza o decote e babados na barra que garantem movimento a cada passo. Perfeito para festas na praia, baladas ou para onde você queira se sentir poderosa.",
        "imagem": "https://drive.google.com/thumbnail?id=1MLL3YjLFlP8EsQ-mR9-nQq0kf8iNn1Pg&sz=w1000",
        "categoria": "vestidos"
    },
    {
        "id": 2,
        "nome": "Vestido Barra Coral",
        "preco": 110.00,
        "descricao": "O Caribe em cada fio. O Barra Coral tem twist frontal que cria volume no colo e recortes laterais que mostram na medida certa. Um vestido que pede sol, margarita e boa música vestindo sua melhor noite de verão.",
        "imagem": "https://drive.google.com/thumbnail?id=1mpCBdACvpZmz9HE4YgGIrEfIrqQe9Olg&sz=w1000",
        "categoria": "vestidos"
    },
    {
        "id": 3,
        "nome": "Conjunto Pôr do Sol Tropical",
        "preco": 80.00,
        "descricao": "Delicado e sofisticado ao mesmo tempo. O Pôr do Sol Tropical é um conjunto de duas peças em crochê off-white com detalhes em conchas douradas que capturam a luz. ",
        "imagem": "https://drive.google.com/thumbnail?id=1pSxl53vvtaBd4Czn1_rJvFsPDopsgDNj&sz=w1000",
        "categoria": "conjuntos"
    },
    {
        "id": 4,
        "nome": "Vestido Areia Dourada",
        "preco": 179.99,
        "descricao": "Feito para quem ama um visual natural e cheio de textura. O Areia Dourada tem aquele tom de areia molhada que combina com tudo — pele bronzeada, sandália dourada, fim de tarde. O crochê artesanal garante que nenhuma peça é igual à outra.",
        "imagem": "https://drive.google.com/thumbnail?id=1Bz2d_SlRsQQqAHD712JmOYTXSNJ82N6t&sz=w1000",
        "categoria": "vestidos"
    },
    {
        "id": 5,
        "nome": "Conjunto Maré Alta",
        "preco": 85.00,
        "descricao": "Duas peças, infinitas combinações. O Maré Alta tem franjas que balançam com o vento e caimento que valoriza o corpo em movimento. Use o top com jeans para um jantar casual, ou o conjunto completo para arrasar na orla. É aquela peça que você vai querer usar até desgastar.",
        "imagem": "https://drive.google.com/thumbnail?id=1Iy6g9-K4C_JP1Y46tEtqucZsOZaJKDsw&sz=w1000",
        "categoria": "conjuntos"
    },
    {
        "id": 6,
        "nome": "Vestido Estrela do Mar",
        "preco": 120.00,
        "descricao": "Um vestido que conta uma história. O Estrela do Mar tem estrelinhas bordadas à mão em tons de rosa e azul sobre crochê off-white — cada detalhe feito com cuidado e intenção. Para se sentir única onde quer que esteja.",
        "imagem": "https://drive.google.com/thumbnail?id=1Myf3qW6BobigvUvpa7vVJM1tUA25HWUF&sz=w1000",
        "categoria": "vestidos"
    }
]

@app.route('/')
def index():
    return render_template('index.html', produtos=PRODUTOS)

if __name__ == '__main__':
    app.run(debug=True)
