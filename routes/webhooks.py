from flask import Blueprint, request, jsonify, current_app
from moysklad.client import MoyskladClient
from utils.security import verify_webhook_signature

webhooks_bp = Blueprint('webhooks', __name__)

@webhooks_bp.route('/webhook/moysklad', methods=['POST'])
def handle_moysklad_webhook():
    """
    Обработчик вебхуков от МойСклад
    """
    # Проверка подписи (если используется)
    # signature = request.headers.get('X-Moysklad-Signature')
    # if not verify_webhook_signature('your-secret-key', signature):
    #     return jsonify({'error': 'Invalid signature'}), 401
    
    data = request.json
    current_app.logger.info(f"Received webhook: {data}")
    
    # Обработка различных типов событий
    event_type = data.get('event', '')
    
    if 'customerorder' in event_type:
        handle_customer_order_event(data)
    
    return jsonify({'status': 'success'}), 200

def handle_customer_order_event(data):
    """
    Обработка событий связанных с заказами покупателей
    """
    action = data.get('action', '')
    order_data = data.get('data', {})
    
    current_app.logger.info(f"Customer order event: {action}")
    
    if action == 'CREATE':
        # Обработка создания заказа
        process_new_order(order_data)
    elif action == 'UPDATE':
        # Обработка обновления заказа
        process_updated_order(order_data)
    elif action == 'DELETE':
        # Обработка удаления заказа
        process_deleted_order(order_data)

def process_new_order(order_data):
    """Обработка нового заказа"""
    current_app.logger.info(f"New order created: {order_data.get('id')}")
    # Здесь можно добавить логику обработки нового заказа

def process_updated_order(order_data):
    """Обработка обновленного заказа"""
    current_app.logger.info(f"Order updated: {order_data.get('id')}")
    # Здесь можно добавить логику обработки обновленного заказа

def process_deleted_order(order_data):
    """Обработка удаленного заказа"""
    current_app.logger.info(f"Order deleted: {order_data.get('id')}")
    # Здесь можно добавить логику обработки удаленного заказа