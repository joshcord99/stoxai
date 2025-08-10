import os
from datetime import timedelta

class Config:
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'joshuacordial')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')
    POSTGRES_DATABASE = os.environ.get('POSTGRES_DATABASE', 'stock_analyst')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    
    CORS_ORIGINS = [
        'http://localhost:3000', 
        'http://localhost:5173', 
        'http://localhost:5174',
        'http://127.0.0.1:5173', 
        'http://127.0.0.1:5174',
        'http://localhost:4173', 
        'http://127.0.0.1:4173',
        'https://stoxai.netlify.app',
        'https://stoxai-backend.onrender.com'
    ]
