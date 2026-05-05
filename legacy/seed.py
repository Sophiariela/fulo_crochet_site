import json
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

with open("produtos.json", "r", encoding="utf-8") as f:
    produtos = json.load(f)

conn = psycopg2.connect(
    dbname="fulo",
    user="u0_a485",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

for produto in produtos:
    cur.execute("""
        INSERT INTO produtos (nome, preco, descricao, imagem, categoria)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        produto["nome"],
        produto["preco"],
        produto["descricao"],
        produto["imagem"],
        produto["categoria"]
    ))

conn.commit()
cur.close()
conn.close()

print("Produtos inseridos com sucesso!")
