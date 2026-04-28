from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fulo_user:fl_jnyfer_crochet@localhost/fulo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Produto
class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(500))
    categoria = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Produto {self.nome}>'

# Criar tabelas
with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso!")

if __name__ == '__main__':
    app.run(debug=True)
