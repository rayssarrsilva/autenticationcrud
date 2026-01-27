import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Cookies protegidos
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Em produção deve ser True (HTTPS)
    SESSION_COOKIE_SAMESITE = 'Lax'

    @staticmethod
    def validate():
        missing = []
        for key in ['SECRET_KEY', 'MAIL_USERNAME', 'MAIL_PASSWORD']:
            if not getattr(Config, key):
                missing.append(key)
        if missing:
            raise RuntimeError(f"Variáveis de ambiente ausentes: {', '.join(missing)}")
