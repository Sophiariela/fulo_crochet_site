from flask import Flask, render_template

app = Flask(__name__)

PRODUTOS = [
    {
        "id": 1,
        "nome": "Vestido Bahia Blue",
        "preco": 200.00,
        "descricao": "Crochê halter neck em azul royal.",
        "imagem": "https://drive.google.com/thumbnail?id=1MLL3YjLFlP8EsQ-mR9-nQq0kf8iNn1Pg&sz=w1000",
        "categoria": "vestidos"
    },
    {
        "id": 2,
        "nome": "Vestido Barra Coral",
        "preco": 110.00,
        "descricao": "Tomara que caia com twist frontal e recortes laterais. Cor de Caribe.",
        "imagem": "https://drive.google.com/thumbnail?id=1mpCBdACvpZmz9HE4YgGIrEfIrqQe9Olg&sz=w1000",
        "categoria": "vestidos"
    },
    {
        "id": 3,
        "nome": "Conjunto Pôr do Sol Tropical",
        "preco": 200.00,
        "descricao": "Duas peças off-white com conchas douradas. Delicado e sofisticado.",
        "imagem": "https://drive.google.com/thumbnail?id=1pSxl53vvtaBd4Czn1_rJvFsPDopsgDNj&sz=w1000",
        "categoria": "conjuntos"
    },
    {
        "id": 4,
        "nome": "Vestido Areia Dourada",
        "preco": 300.00,
        "descricao": "Tom de areia, textura rica, caimento que abraça.",
        "imagem": "https://drive.google.com/thumbnail?id=1Bz2d_SlRsQQqAHD712JmOYTXSNJ82N6t&sz=w1000",
        "categoria": "vestidos"
    },
    {
        "id": 5,
        "nome": "Conjunto Maré Alta",
        "preco": 270.00,
        "descricao": "Franjas que balançam, duas peças, infinitas combinações.",
        "imagem": "https://drive.google.com/thumbnail?id=1Iy6g9-K4C_JP1Y46tEtqucZsOZaJKDsw&sz=w1000",
        "categoria": "conjuntos"
    },
    {
        "id": 6,
        "nome": "Vestido Estrela do Mar",
        "preco": 270.00,
        "descricao": "Estrelinhas bordadas à mão sobre crochê off-white.",
        "imagem": "https://drive.google.com/thumbnail?id=1Myf3qW6BobigvUvpa7vVJM1tUA25HWUF&sz=w1000",
        "categoria": "vestidos"
    }
]

@app.route('/')
def index():
    return render_template('index.html', produtos=PRODUTOS)

if __name__ == '__main__':
    app.run(debug=True)
