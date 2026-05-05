import requests
import json
from bs4 import BeautifulSoup

url = "https://fulo-crochet.onrender.com"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

produtos = []

cards = soup.find_all("div", class_="card")

for card in cards:
    nome = card.find("h2", class_="card-titulo").get_text(strip=True)
    preco = (
        card.find("p", class_="card-preco")
        .get_text(strip=True)
        .replace("R$", "")
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )
    descricao = card.find("p", class_="card-descricao").get_text(strip=True)
    imagem = card.find("img")["src"]
    categoria = card.get("data-categoria", "geral")

    produtos.append({
        "nome": nome,
        "preco": float(preco),
        "descricao": descricao,
        "imagem": imagem,
        "categoria": categoria
    })

with open("produtos.json", "w", encoding="utf-8") as f:
    json.dump(produtos, f, ensure_ascii=False, indent=2)

print(f"{len(produtos)} produtos extraídos com sucesso.")
