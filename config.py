import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Force SQLite for development in this environment
    SQLALCHEMY_DATABASE_URI = "postgresql://u0_a485@localhost:5432/fulo"
    
    # Mercado Pago
    MP_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN', 'TEST-YOUR-ACCESS-TOKEN')
    MP_PUBLIC_KEY = os.getenv('MP_PUBLIC_KEY', 'TEST-YOUR-PUBLIC-KEY')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://yourdomain.com/checkout/webhook')
