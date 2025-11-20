import hmac
import hashlib
from flask import request, current_app

def verify_webhook_signature(secret_key, signature_header):
    """
    Проверка подписи вебхука от МойСклад
    """
    if not signature_header:
        return False
    
    # Генерация подписи для проверки
    body = request.get_data()
    generated_signature = hmac.new(
        secret_key.encode('utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(generated_signature, signature_header)

def validate_access_token(access_token):
    """
    Базовая валидация токена доступа
    """
    if not access_token:
        return False
    
    # Здесь можно добавить дополнительную логику валидации
    # Например, проверку формата токена
    
    return True