# Fulo Crochet

> *Do barro, pela mão, pra você.*

Loja virtual da Fulô Crochet ([@fulocrochet_](https://www.instagram.com/fulocrochet_)), marca artesanal de Salvador, Bahia.  
Desenvolvido por Sophia Riela — [The Fashion Codes](https://www.instagram.com/thefashioncodes_).



## Tecnologias

- **Python 3 + Flask** — backend e renderização de templates
- **Jinja2** — templating HTML
- **HTML / CSS / JavaScript** — frontend estático
- **Render** — deploy e hospedagem



## Estrutura do projeto

```
fulo/
├── app.py                  # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── Procfile                # Configuração de processo (Render)
├── build.sh                # Script de build para deploy
├── .gitignore
├── static/
│   ├── images/
│   │   └── banner.png
│   ├── style.css
│   └── main.js
└── templates/
    └── index.html
```



## Como rodar localmente

Pré-requisito: Python 3 instalado. Compatível com Termux (Android).

```bash
git clone https://github.com/SophiaRiela/fulo_crochet_site.git
cd fulo_crochet_site
pip install -r requirements.txt
flask run
```

Acesse em: `http://127.0.0.1:5000`



## Deploy

O projeto está hospedado no [Render](https://render.com).  
O deploy é ativado automaticamente a cada push na branch `main`.

```bash
git add .
git commit -m "descrição da mudança"
git push
```



## Funcionalidades

- Catálogo de produtos com filtro por categoria (Vestidos, Conjuntos, Tops, Saias, Acessórios)
- Botão de pedido direto via WhatsApp com mensagem pré-preenchida
- Botão flutuante do WhatsApp
- Layout responsivo para dispositivos móveis
- Animação de entrada nos cards de produto



## Créditos

**Marca:** Jhennyfer Arcanjo ([@fulocrochet_](https://www.instagram.com/fulocrochet_))  
**Desenvolvimento:** Sophia Riela — The Fashion Codes ([@thefashioncodes_](https://www.instagram.com/thefashioncodes_))
