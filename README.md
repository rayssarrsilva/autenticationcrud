# Autentication CRUD – Flask System  
Aplicação web segura para cadastro, login, logout e redefinição de senha via tokens enviados por e-mail.

## Demo
![autenticacaosimples](https://github.com/user-attachments/assets/c76bae72-9702-4c67-96f0-99f014bfdfa8)

## Funcionalidades
1. Registro de usuários com validação e feedback.
2. Login e logout com mensagens de sucesso/erro.
3. Redefinição de senha via e-mail com token seguro e expiração.
4. Dashboard personalizado com seção de blog “kawaii”.
5. API REST para registro, login e reset de senha.
6. Templates responsivos com Bootstrap 5, Google Fonts, Font Awesome e Material Icons.
7. Mensagens flash interativas com SweetAlert2.

## Tech Stack
1. Frontend: Jinja2 templates, Bootstrap 5, CSS customizado, SweetAlert2.
2. Backend: Flask (Python), Flask-Login, Flask-Migrate.
3. Database: SQLite (dev), PostgreSQL (produção).
4. Serviços externos: Brevo API para envio de e-mails.

## Setup 
1. Clone o repositório
```
git clone https://github.com/rayssarrsilva/autenticationcrud.git
cd autenticationcrud
```
2. Crie e ative um abiente virtual
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3. Instale dependências
```
pip install -r requirements.txt
```
4. Configure as variáveis de ambiente em .env
```
SECRET_KEY
DATABASE_URL (SQLite para dev, PostgreSQL para produção)
MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD
BREVO_API_KEY
```
5. Inicialize o banco
```
flask db init
flask db migrate
flask db upgrade
```
6. Rode localmente
```
python app.py
http://127.0.0.1:5000
```

## O que aprendi
1. Implementação de autenticação segura com Flask-Login e hashing de senhas.
2. Uso de tokens temporários para reset de senha com itsdangerous.
3. Configuração de headers de segurança (CSP, HSTS, X-Frame-Options).
4. Deploy em Render.com com Gunicorn e variáveis de ambiente.
5. Criação de UI responsiva e divertida com Bootstrap + animações CSS/JS.
6. Integração com serviço externo de e-mail (Brevo API).
7. Profissional vibe coding
