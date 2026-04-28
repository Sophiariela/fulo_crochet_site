from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def get_produtos():
    conn = psycopg2.connect(
        dbname="fulo_db",
        user="fulo_user",
        password="",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("SELECT id, nome, preco, descricao, categoria, imagem FROM produtos ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    produtos = []
    for row in rows:
        produtos.append({
            "id": row[0],
            "nome": row[1],
            "preco": row[2],
            "descricao": row[3],
            "categoria": row[4],
            "imagem": row[5]
        })
    return produtos

@app.route('/')
def index():
    produtos = get_produtos()
    return render_template('index.html', produtos=produtos)

if __name__ == '__main__':
    app.run(debug=True)
