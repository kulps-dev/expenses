import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Конфигурация приложения"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = os.environ.get('DEBUG', False)
    
    # Настройки МойСклад
    MOYSKLAD_API_URL = 'https://api.moysklad.ru/api/remap/1.2'
    APP_ENDPOINT_BASE = 'http://89.223.65.166'
    
    # Порт для запуска приложения
    PORT = int(os.environ.get('PORT', 5000))