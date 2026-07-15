from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)
auth_bp.strict_slashes = False

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.home'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado.', 'danger')
            return redirect(url_for('auth.register'))

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('public.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            
            flash('Login realizado com sucesso!', 'success')
            
            # Redirect to next page or default
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
                
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('public.home'))

        flash('Email ou senha inválidos', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.home'))

@auth_bp.route('/account')
@login_required
def minha_conta():
    return render_template('public/account.html', user=current_user)

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            # In a real app, send email here. Printing for demo.
            print(f"DEBUG: Password reset link: {url_for('auth.reset_password', token=token, _external=True)}")
            flash('Um link de recuperação foi enviado para seu email (simulado no console).', 'info')
        else:
            flash('Email não encontrado.', 'warning')
    return render_template('auth/reset_request.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter(
        User.reset_token == token,
        User.reset_token_expiration > datetime.utcnow()
    ).first()
    
    if not user:
        flash('Token inválido ou expirado.', 'danger')
        return redirect(url_for('auth.reset_request'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        user.set_password(password)
        user.reset_token = None
        user.reset_token_expiration = None
        db.session.commit()
        flash('Sua senha foi atualizada!', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/reset_password.html')
