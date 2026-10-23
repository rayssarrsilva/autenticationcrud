import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from config import Config
from flask_migrate import Migrate
import requests


# Inicialização
app = Flask(__name__)
app.config.from_object(Config)
Config.validate()

db = SQLAlchemy(app)
#mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelo
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# envio email
def send_email(to, subject, html_content):
    api_key = os.environ.get("BREVO_API_KEY")
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    data = {
        "sender": {"name": "InterfaceAuth", "email": os.environ.get("MAIL_USERNAME")},
        "to": [{"email": to}],
        "subject": subject,
        "htmlContent": html_content
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code

# ---------------- ROTAS HTML ----------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email já cadastrado.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(username=form.username.data).first():
            flash('Usuário já existe.', 'danger')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('welcome'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('login'))

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = s.dumps(user.email, salt='reset-senha')
            link = url_for('reset_token', token=token, _external=True)
            html_content = f"""
            <p>Olá,</p>
            <p>Clique no link abaixo para redefinir sua senha:</p>
            <p><a href="{link}">Redefinir senha</a></p>
            """
            try:
                status = send_email(user.email, "Redefinir sua senha", html_content)
                if status in [200, 201]:
                    flash('Email enviado com instruções!', 'info')
                else:
                    flash('Erro ao enviar email. Tente novamente mais tarde.', 'danger')
            except Exception as e:
                app.logger.error(f"Erro ao enviar email: {e}")
                flash('Erro ao enviar email. Tente novamente mais tarde.', 'danger')
        else:
            flash('Email não encontrado.', 'danger')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    try:
        email = s.loads(token, salt='reset-senha', max_age=3600)
    except SignatureExpired:
        flash('Token expirado.', 'warning')
        return redirect(url_for('reset_request'))
    except BadSignature:
        flash('Token inválido.', 'danger')
        return redirect(url_for('reset_request'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user.password_hash = hashed_pw
        db.session.commit()
        flash('Senha atualizada com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)

# ---------------- ROTAS API ----------------
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({"message": "Dados inválidos"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email já cadastrado"}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Usuário já existe"}), 400
    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], email=data['email'], password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Conta criada com sucesso!"}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Dados inválidos"}), 400
    user = User.query.filter_by(email=data.get('email')).first()
    if user and check_password_hash(user.password_hash, data.get('password')):
        return jsonify({"message": "Login realizado com sucesso!"}), 200
    return jsonify({"message": "Email ou senha incorretos."}), 401

@app.route('/api/reset_password', methods=['POST'])
def api_reset_request():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"message": "Dados inválidos"}), 400
    user = User.query.filter_by(email=data.get('email')).first()
    if user:
        token = s.dumps(user.email, salt='reset-senha')
        link = url_for('reset_token', token=token, _external=True)
        html_content = f"""
        <p>Olá,</p>
        <p>Clique no link abaixo para redefinir sua senha:</p>
        <p><a href="{link}">Redefinir senha</a></p>
        """
        try:
            status = send_email(user.email, "Redefinir sua senha", html_content)
            if status in [200, 201]:
                return jsonify({"message": "Email enviado com instruções!"}), 200
            else:
                return jsonify({"message": "Erro ao enviar email"}), 500
        except Exception as e:
            app.logger.error(f"Erro ao enviar email: {e}")
            return jsonify({"message": "Erro interno"}), 500
    return jsonify({"message": "Email não encontrado"}), 404
        
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;"
    )
    return response        
# ---------------- MAIN ----------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
