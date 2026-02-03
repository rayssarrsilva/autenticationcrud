# 🌸 Flask System ✨

![autenticacaosimples](https://github.com/user-attachments/assets/c76bae72-9702-4c67-96f0-99f014bfdfa8)

## 📖 Overview
A **Flask-based web application** designed with a strong focus on **security, user experience, and kawaii-inspired design**.  
It provides:
- User authentication (register, login, logout)  
- Password reset via secure email tokens  
- REST API endpoints for integration  
- Responsive templates with **Bootstrap 5**, **Google Fonts**, **Font Awesome**, **Material Icons**, and **SweetAlert2** flash messages  
- Playful animations and interactions for a delightful UI/UX  

---

## 🏗️ Architecture
- **Framework**: Flask (Python)

- **ORM**: SQLAlchemy

- **Autenticação**: Flask-Login

- **Forms & Validation**: WTForms

- **Email Service: Brevo API (via requests)**

- **Token Management**: itsdangerous (URLSafeTimedSerializer)

- **igrations**: Flask-Migrate

- **Frontend: Jinja2 templates com herança (base.html)**

- **Styling: Bootstrap 5, Google Fonts (Inter, Poppins), Font Awesome, Material Icons**

- **Mensagens Flash**: SweetAlert2
---

## 🗄️ Database
- **Default:** SQLite (development)  
- **Production:** PostgreSQL (via `DATABASE_URL`)  
- **Migrations:** Managed with Flask-Migrate  
- **User Model:**  
  - `id` (Primary Key)  
  - `username` (Unique, required)  
  - `email` (Unique, required)  
  - `password_hash` (Securely hashed)  

---

## 🔐 Security
- **Password Hashing**: `generate_password_hash e check_password_hash`

- **CSRF Protection**: `form.hidden_tag()` in all forms

- **Token-based Reset**: itsdangerous.URLSafeTimedSerializer with expiration

- **Secure Headers**:

- **X-Content-Type-Options**: nosniff

- **X-Frame-Options**: DENY

- **Strict-Transport-Security**: `max-age=31536000; includeSubDomains`

- **Content-Security-Policy**: `default-src 'self'`

- **Error Logging**: error sending email logged in with `app.logger.error`

---

## 🔗 User Flow
1. **Index (`/`)** → Landing page with options to login or register  
2. **Register (`/register`)** → Create account with validation and feedback  
3. **Login (`/login`)** → Authenticate with success/error messages  
4. **Logout (`/logout`)** → End session securely  
5. **Reset Request (`/reset_password`)** → Request password reset via email  
6. **Reset Token (`/reset_password/<token>`)** → Update password securely  
7. **Welcome (`/welcome`)** → Personalized dashboard with kawaii blog section  

---

## 📡 API Endpoints
- `POST /api/register` → Create user  
- `POST /api/login` → Authenticate user  
- `POST /api/reset_password` → Request password reset  

Example JSON responses:
```json
{ "message": "Account created successfully!" }
{ "message": "Email already registered" }
{ "message": "Invalid email or password." }
```

## 🎨 Design & Templates
- **Template Inheritance:** All pages extend `base.html`  
- **Navbar:** Dynamic (changes based on login state)  
- **Cards:** Rounded corners, shadows, modern look  
- **Fonts:** `Inter` and `Poppins` via Google Fonts  
- **Icons:** Font Awesome + Material Icons  
- **Flash Messages:** SweetAlert2 with category-based icons (success, error, info, warning)  
- **Animations:**  
  - CSS: bounce, pulse, spin, glow, rainbow, wiggle, heartbeat, flip, shimmer, swing, fadeGlow, float  
  - JavaScript: typing effect, icon hover bounce, click spin, article flip  

---

## 🚀 Deployment
- **Platform: Render.com**

- **WSGI Server: Gunicorn**

- **Environment Variables**:
- SECRET_KEY
- DATABASE_URL
- MAIL_SERVER
- MAIL_PORT
- MAIL_USE_TLS
- MAIL_USERNAME
- MAIL_PASSWORD
- BREVO_API_KEY

**Production Notes**:
- Debug desativado (debug=False)
- HTTPS forçado com HSTS
- Logs monitorados para erros de email 
---

## 📂 Project Structure
project/
│── app.py                            # Main Flask application
│── config.py                      # Configuration settings
│── forms.py                        # WTForms definitions
│── models.py                      # SQLAlchemy models
│── migrations/         # Database migrations
│── templates/          # Jinja2 templates
│   │── base.html
│   │── index.html
│   │── login.html
│   │── register.html
│   │── reset_request.html
│   │── reset_token.html
│   │── welcome.html
│── static/
│   │── style.css              # Global styles
│   │── scripts.js            # Kawaii animations

---

## 🛠️ Best Practices Implemented
- **Clean Code:** Clear naming, modular functions  
- **DRY Principle:** Template inheritance avoids duplication  
- **UX First:** Feedback for every user action  
- **Security First:** Hashing, CSRF, secure headers, token expiration  
- **Deployment Ready:** Configurable via environment variables  
- **Design:** Modern, kawaii-inspired, responsive  

---

## 📌 Running Locally
```bash
# Clone repository
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---
# 🛠️ Local Setup Tutorial

Follow these steps to clone and run the **Flask Coquette System** on your machine.

---

## 📂 1. Clone the Repository
```bash
# Clone the repository from GitHub
git clone https://github.com/your-username/flask-coquette-system.git
```
# Enter the project folder
```cd name_of_folder```

---
# Create virtual environment
```python -m venv venv```

---
# Activate environment
```source venv/bin/activate   # Linux/Mac```
```venv\Scripts\activate      # Windows```

---
# Install dependencies
```pip install -r requirements.txt```

---
# Flask secret key
``` SECRET_KEY=your_secret_key_here ```

---
# Database URL (PostgreSQL in production, SQLite for dev)
```DATABASE_URL=sqlite:///site.db```

# Example for PostgreSQL:
```# DATABASE_URL=postgresql://user:password@localhost/dbname```

---
# Create a .env file in the project root with the following variables:
## Mail configuration
```MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
```
---
# Initialize the Database
```
flask db init      # only first time
flask db migrate   # generate migration
flask db upgrade   # apply migration
```

---
# Run the Application
```python app.py```

---
The app will be available at:
http://127.0.0.1:5000
---

