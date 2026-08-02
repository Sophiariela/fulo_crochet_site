import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Fallback to SQLite if DATABASE_URL is not provided
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'fulo.db')}"

    MP_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN', 'TEST-YOUR-ACCESS-TOKEN')
    MP_PUBLIC_KEY = os.getenv('MP_PUBLIC_KEY', 'TEST-YOUR-PUBLIC-KEY')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://yourdomain.com/checkout/webhook')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

    # Enquanto a conta oficial da Fulô no Mercado Pago não estiver vinculada,
    # o checkout roda em modo homologação/showcase (nenhuma cobrança real é feita).
    # Defina PAYMENTS_ENABLED=true no ambiente quando as credenciais oficiais entrarem em produção.
    PAYMENTS_ENABLED = os.getenv('PAYMENTS_ENABLED', 'false').strip().lower() in ('1', 'true', 'yes')

    SOCIALS_INSTAGRAM = 'https://www.instagram.com/aster.ops'