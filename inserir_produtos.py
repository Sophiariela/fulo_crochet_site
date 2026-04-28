import psycopg2

conn = psycopg2.connect("postgresql://fulo_db_user:uBnTaAWuT8V8nDZjIHEynM2VtaUx7PIx@dpg-d7ogqj9f9bms73dmv080-a.ohio-postgres.render.com/fulo_db")
cur = conn.cursor()

produtos = [
    (1, "Vestido Bahia Blue", 200.00, "Vestido halter neck em crochê artesanal, linha 100% algodão azul royal vibrante.", "vestidos", "/static/imagens/vestido-bahia-blue.jpg"),
    (2, "Conjunto Flor de Maio", 190.00, "Conjunto composto por top e saia mini em crochê artesanal, linha 100% algodão off-white.", "conjuntos", "/static/imagens/conjunto-flor-de-maio.png"),
    (3, "Vestido Nevoa", 300.00, "Vestido curto em crochê artesanal, linha 100% algodão off-white. Halter neck com costas abertas.", "vestidos", "/static/imagens/vestido-nevoa.png"),
    (4, "Vestido Areia Dourada", 300.00, "Vestido assimétrico ombro único em crochê artesanal, linha 100% algodão off-white.", "vestidos", "/static/imagens/vestido-areia-dourada.png"),
    (5, "Top Terra Preta", 70.00, "Top triangular halter neck em crochê artesanal, 100% poliamida na cor chocolate.", "tops", "/static/imagens/top-terra-preta.png"),
    (6, "Top Orquidea", 90.00, "Top em crochê artesanal, linha 100% algodão off-white com aplicação de orquídea multicolorida.", "tops", "/static/imagens/top-orquidea.png"),
    (7, "Saia Piteira", 100.00, "Saia mini em crochê artesanal, linha 100% algodão off-white. Cintura alta com cordão regulável.", "saias & shorts", "/static/imagens/saia-piteira.png"),
    (8, "Vestido Estrela do Mar", 270.00, "Vestido em crochê artesanal, linha 100% algodão branca com aplicações de estrelas-do-mar.", "vestidos", "/static/imagens/vestido-estrela-do-mar.png"),
    (9, "Conjunto Noite Selvagem", 260.00, "Conjunto em crochê artesanal, linha 100% algodão cru com bordado de onça pintada.", "conjuntos", "/static/imagens/conjunto-noite-selvagem.png"),
    (10, "Conjunto Liana", 300.00, "Conjunto em crochê artesanal, linha 100% algodão bicolor com franjas douradas.", "conjuntos", "/static/imagens/conjunto-liana.jpg"),
    (11, "Vestido Acai", 250.00, "Vestido em crochê artesanal, linha 100% algodão na cor vinho. Alças finas, corte reto.", "vestidos", "/static/imagens/vestido-acai.png"),
    (12, "Vestido Jabuticaba", 280.00, "Vestido em crochê artesanal, linha 100% algodão vinho escuro. Alças finas com pingentes dourados.", "vestidos", "/static/imagens/vestido-jabuticaba.png"),
    (13, "Vestido Sol do Tapajos", 220.00, "Vestido em crochê artesanal, linha 100% algodão cru. Alças finas com pingentes dourados.", "vestidos", "/static/imagens/vestido-sol-do-tapajos.jpg"),
    (14, "Top Arara", 120.00, "Top tomara-que-caia em crochê artesanal com bordado de arara-azul em ponto tapeçaria.", "tops", "/static/imagens/top-arara.png"),
    (15, "Top Por do Amazonas", 50.00, "Top em crochê artesanal, linha 100% algodão laranja queimado. Modelo triângulo.", "tops", "/static/imagens/top-por-do-amazonas.png"),
    (16, "Top Cacau", 50.00, "Top em crochê artesanal, linha 100% algodão marrom. Modelo triângulo com alças reguláveis.", "tops", "/static/imagens/top-cacau.png"),
    (17, "Top Cocada", 100.00, "Top colete em crochê artesanal, linha 100% algodão cru. Modelo halter com abertura frontal.", "tops", "/static/imagens/top-cocada.png"),
    (18, "Top Flor de Orquidea", 90.00, "Top em crochê artesanal, linha 100% algodão branco com aplicação de orquídea em relevo.", "tops", "/static/imagens/top-flor-de-orquidea.png"),
    (19, "Top Raiz Brasileira", 70.00, "Top em crochê artesanal, linha 100% algodão verde com detalhes nas cores do Brasil.", "tops", "/static/imagens/top-raiz-brasileira.png"),
    (20, "Bolsa Buriti", 100.00, "Bolsa em crochê artesanal, linha 100% algodão marrom. Modelo meia-lua com alça em miçangas.", "acessorios", "/static/imagens/bolsa-buriti.jpg"),
    (21, "Bandana Folha Amazonica", 70.00, "Bandana em crochê artesanal, linha 100% algodão verde. Formato aba larga com amarração.", "acessorios", "/static/imagens/bandana-folha-amazonica.png"),
    (22, "Top Sereia Azul", 75.00, "Top triângulo em crochê artesanal, fio azul royal com aplicação de paetes circulares.", "tops", "/static/imagens/top-sereia-azul.png"),
    (23, "Top Ouro de Midas", 75.00, "Top triângulo em crochê artesanal com aplicação de paetes dourados. Efeito metálico exclusivo.", "tops", "/static/imagens/top-ouro-de-midas.png"),
    (24, "Top Lua Cheia", 85.00, "Top triângulo assimétrico em crochê artesanal, algodão off white com argolas e moedas.", "tops", "/static/imagens/top-lua-cheia.png"),
    (25, "Top Ondas do Caribe", 85.00, "Top triângulo em crochê artesanal, fio azul. Modelagem assimétrica com trama aberta.", "tops", "/static/imagens/top-ondas-do-caribe.png"),
    (26, "Top Noite Estrelada", 85.00, "Top triângulo em crochê artesanal, fio preto. Modelagem assimétrica com trama aberta.", "tops", "/static/imagens/top-noite-estrelada.png"),
    (27, "Top Galaxia Profunda", 85.00, "Top triângulo em crochê artesanal, fio preto. Modelagem assimétrica com alça única.", "tops", "/static/imagens/top-galaxia-profunda.png"),
    (28, "Biquini Rainha Negra", 120.00, "Conjunto biquíni em crochê artesanal, fio preto com miçangas e correntes douradas.", "biquinis", "/static/imagens/biquini-rainha-negra.png"),
    (29, "Biquini Ceu de Verao", 120.00, "Conjunto biquíni em crochê artesanal, fio azul claro. Top triângulo com trama em ponto renda.", "biquinis", "/static/imagens/biquini-ceu-de-verao.png"),
    (30, "Biquini Nevoa de Prata", 120.00, "Conjunto biquíni em crochê artesanal, fio prata. Efeito metálico sutil e delicado.", "biquinis", "/static/imagens/biquini-nevoa-de-prata.png"),
    (31, "Biquini Ipanema Gold", 120.00, "Conjunto biquíni em crochê artesanal, listras preto e dourado com argolas douradas.", "biquinis", "/static/imagens/biquini-ipanema-gold.png"),
    (32, "Conjunto Moca Baiana", 120.00, "Conjunto em crochê artesanal, fio multicolor. Top triângulo e sainha de cintura alta.", "conjuntos", "/static/imagens/conjunto-moca-baiana.png"),
    (33, "Conjunto Nevoa", 200.00, "Conjunto em crochê artesanal, algodão off white. Top com alça fina e sainha com franjas.", "conjuntos", "/static/imagens/conjunto-nevoa.png"),
    (34, "Vestido Brasileirinha", 270.00, "Vestido tomara-que-caia em crochê artesanal, fio multicolor com listras horizontais.", "vestidos", "/static/imagens/vestido-brasileirinha.jpg"),
]

for p in produtos:
    cur.execute("INSERT INTO produtos (id, nome, preco, descricao, categoria, imagem) VALUES (%s, %s, %s, %s, %s, %s)", p)

conn.commit()
cur.close()
conn.close()
print("34 produtos inseridos!")
