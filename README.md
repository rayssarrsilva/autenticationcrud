# Flask authentication

**English** · [Português](#português)

Sign-up, sign-in, sign-out and password reset by email, built with Flask. A study project on how authentication works under the hood: password hashing, sessions, signed tokens that expire, and security headers.

![Sign-up, sign-in and the welcome page](https://github.com/user-attachments/assets/c76bae72-9702-4c67-96f0-99f014bfdfa8)

## Features

- **Sign-up** with server-side validation: valid email, unique username and email, password with at least 8 characters, upper and lower case, a number and a symbol.
- **Sign-in and sign-out** with Flask-Login; the welcome page is only reachable when signed in.
- **Password reset by email:** a signed link (itsdangerous) that expires after 1 hour, sent through the Brevo API.
- **JSON endpoints:** `POST /api/register`, `POST /api/login` (checks the credentials, does not start a session) and `POST /api/reset_password`.
- **Security headers** on every response: Content Security Policy, HSTS, `X-Frame-Options: DENY` and `X-Content-Type-Options: nosniff`.
- **CSRF protection** on every HTML form (Flask-WTF), and `HttpOnly` + `SameSite=Lax` session cookies.

## Built with

| Layer | Tools |
| --- | --- |
| Backend | Python, Flask 3, Flask-Login, Flask-WTF / WTForms, itsdangerous |
| Database | SQLAlchemy 2 with Flask-Migrate (Alembic); SQLite locally, PostgreSQL in production |
| Frontend | Jinja2 templates, Bootstrap 5, SweetAlert2 |
| Email | Brevo transactional email API |
| Deploy | Gunicorn (`Procfile`) |

## Run it locally

```bash
git clone https://github.com/rayssarrsilva/autenticationcrud.git
cd autenticationcrud
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```
SECRET_KEY=          # generate one with: python chave.py
MAIL_USERNAME=       # sender address registered in Brevo
MAIL_PASSWORD=       # required by the config check
BREVO_API_KEY=       # only needed to actually send reset emails
DATABASE_URL=        # optional; defaults to SQLite (site.db)
```

Create the tables and start the app:

```bash
flask db init
flask db migrate -m "users"
flask db upgrade
python app.py                   # http://127.0.0.1:5000
```

`psycopg2` is only needed for PostgreSQL. If it fails to install on your machine, use `psycopg2-binary` locally.

## What I would do next

Written down after reviewing my own code with a QA eye:

- Answer "if this email exists, we sent a link" on password reset, instead of saying whether the email is registered (prevents account enumeration).
- Limit sign-in and reset attempts (Flask-Limiter is already in `requirements.txt` but not wired in).
- Set `SESSION_COOKIE_SECURE = True` in production.
- Commit the `migrations/` folder so `flask db upgrade` in the `Procfile` works on a fresh deploy.
- Add automated tests with pytest and Flask's test client.

## What I learned

- Never store passwords: store a salted hash (`werkzeug.security`) and compare hashes.
- Signed, time-limited tokens make a reset link safe to email without saving it in the database.
- Security headers are a few lines of code and block whole classes of attacks (clickjacking, MIME sniffing, injected scripts).
- Keeping secrets in environment variables, never in the repository.

---

## Português

Cadastro, login, logout e redefinição de senha por e-mail, feitos com Flask. Um projeto de estudo para entender como a autenticação funciona por dentro: hash de senha, sessão, tokens assinados com validade e cabeçalhos de segurança.

### Funcionalidades

- **Cadastro** com validação no servidor: e-mail válido, usuário e e-mail únicos, senha com pelo menos 8 caracteres, maiúscula, minúscula, número e símbolo.
- **Login e logout** com Flask-Login; a página de boas-vindas só abre com a pessoa logada.
- **Redefinição de senha por e-mail:** link assinado (itsdangerous) que expira em 1 hora, enviado pela API da Brevo.
- **Endpoints JSON:** `POST /api/register`, `POST /api/login` (confere as credenciais, não abre sessão) e `POST /api/reset_password`.
- **Cabeçalhos de segurança** em toda resposta: Content Security Policy, HSTS, `X-Frame-Options: DENY` e `X-Content-Type-Options: nosniff`.
- **Proteção contra CSRF** em todos os formulários (Flask-WTF) e cookies de sessão `HttpOnly` + `SameSite=Lax`.

### Como rodar

Siga os comandos da seção [Run it locally](#run-it-locally): clonar, criar o ambiente virtual, instalar as dependências, criar o `.env` (gere a `SECRET_KEY` com `python chave.py`), criar as tabelas com `flask db init`, `flask db migrate` e `flask db upgrade` e rodar `python app.py`.

### Próximos passos

Anotados depois de revisar meu próprio código com olhar de QA: resposta igual na redefinição de senha exista ou não o e-mail (evita descobrir contas cadastradas), limite de tentativas no login e na redefinição, `SESSION_COOKIE_SECURE = True` em produção, versionar a pasta `migrations/` e testes automatizados com pytest.
