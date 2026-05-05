from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

admin = Blueprint('admin', __name__)

ADMIN_PASSWORD = generate_password_hash("fl_jnyfer")
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/imagens')

def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated

@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if check_password_hash(ADMIN_PASSWORD, senha):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.painel'))
        flash('Senha incorreta')
    return render_template('admin_login.html')

@admin.route('/admin/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))

@admin.route('/admin')
@login_required
def painel():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, preco, categoria FROM produtos ORDER BY id")
    produtos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_painel.html', produtos=produtos)

@admin.route('/admin/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        foto = request.files['foto']
        filename = secure_filename(foto.filename)
        foto.save(os.path.join(UPLOAD_FOLDER, filename))
        imagem = f'/static/imagens/{filename}'
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO produtos (nome, preco, descricao, categoria, imagem) VALUES (%s, %s, %s, %s, %s)",
                    (nome, preco, descricao, categoria, imagem))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('admin.painel'))
    return render_template('admin_adicionar.html')

@admin.route('/admin/deletar/<int:id>')
@login_required
def deletar(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM produtos WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('admin.painel'))
