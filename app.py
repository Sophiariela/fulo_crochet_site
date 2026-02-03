from flask import Flask, render_template

app = Flask(__name__)

PRODUTOS = [
    {
        "id": 1,
        "nome": "Vestido Bahia Blue",
        "preco": 90.00,
        "descricao": "Vestido em crochê de halter neck confeccionado em fio azul royal vibrante. Com acabamento em babados na barra.",
        "imagem": "https://drive.google.com/thumbnail?id=1MLL3YjLFlP8EsQ-mR9-nQq0kf8iNn1Pg&sz=w1000",
        "categoria": "vestidos"
    },
    {
        "id": 2,
        "nome": "Vestido Barra Coral",
        "preco": 110.00,
        "descricao": "Vestido tomara que caia com twist frontal e recortes estratégicos nas laterais, em tom coral rosado. Inspirado nas cores vibrantes do Caribe.",
        "imagem": "https://drive.google.com/thumbnail?id=1mpCBdACvpZmz9HE4YgGIrEfIrqQe9Olg&sz=w1000",
        "categoria": "vestidos"
    },
    {
        "id": 3,
        "nome": "Conjunto Pôr do Sol Tropical",
        "preco": 80.00,
        "descricao": "Conjunto de duas peças em crochê off-white com aplicações de conchas douradas. O top bandeau apresenta comprimento cropped.",
        "imagem": "https://drive.google.com/thumbnail?id=1pSxl53vvtaBd4Czn1_rJvFsPDopsgDNj&sz=w1000",
        "categoria": "conjuntos"
    },
    {
        "id": 4,
        "nome": "Vestido Areia Dourada",
        "preco": 179.99,
        "descricao": "Vestido elegante em tons de areia com detalhes sofisticados.",
        "imagem": "https://drive.google.com/thumbnail?id=1Bz2d_SlRsQQqAHD712JmOYTXSNJ82N6t&sz=w1000",
        "categoria": "vestidos"
    },
    {
        "id": 5,
        "nome": "Conjunto Maré Alta",
        "preco": 85.00,
        "descricao": "Conjunto versátil de duas peças em crochê, perfeito para um dia na praia ou passeio à beira-mar.",
        "imagem": "https://drive.google.com/thumbnail?id=1Iy6g9-K4C_JP1Y46tEtqucZsOZaJKDsw&sz=w1000",
        "categoria": "conjuntos"
    },
    {
        "id": 6,
        "nome": "Vestido Estrela do Mar",
        "preco": 120.00,
        "descricao": "Vestido delicado em crochê com detalhes que remetem às estrelas do mar, ideal para ocasiões especiais.",
        "imagem": "https://drive.google.com/thumbnail?id=1Myf3qW6BobigvUvpa7vVJM1tUA25HWUF&sz=w1000",
        "categoria": "vestidos"
    }
]

@app.route('/')
def index():
    return render_template('index.html', produtos=PRODUTOS)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
