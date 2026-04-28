from flask import Flask, render_template
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'fulo_secret_2024'
from admin import admin
app.register_blueprint(admin)

DATABASE_URL = os.getenv('DATABASE_URL')

def get_produtos():
    conn = psycopg2.connect(DATABASE_URL)
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
