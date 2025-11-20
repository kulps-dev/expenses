from flask import Flask, request, jsonify, render_template
from config import Config
from moysklad.client import MoyskladClient
from routes.webhooks import webhooks_bp
import logging

def create_app():
    """Фабрика создания приложения Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    
    # Регистрация blueprint'ов
    app.register_blueprint(webhooks_bp)
    
    @app.route('/')
    def index():
        """Главная страница приложения"""
        return jsonify({
            'status': 'success',
            'message': 'МойСклад приложение работает',
            'endpoints': {
                'webhook': '/webhook/moysklad',
                'health': '/health'
            }
        })
    
    @app.route('/health')
    def health_check():
        """Проверка здоровья приложения"""
        return jsonify({'status': 'healthy'})
    
    @app.route('/api/install', methods=['POST'])
    def install_app():
        """
        Обработчик установки приложения
        Вызывается когда пользователь устанавливает приложение в МойСклад
        """
        data = request.json
        app.logger.info(f"App installation data: {data}")
        
        # Здесь можно сохранить информацию об установке
        # Например, access_token, account_id и т.д.
        
        return jsonify({'status': 'success'})
    
    @app.route('/api/customerorders', methods=['GET'])
    def get_customer_orders():
        """
        Получение списка заказов покупателей
        Требует Bearer токен в заголовке Authorization
        """
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        access_token = auth_header.replace('Bearer ', '')
        client = MoyskladClient(access_token)
        
        # Получение параметров запроса
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        orders = client.get_customer_orders(limit=limit, offset=offset)
        
        if orders is None:
            return jsonify({'error': 'Failed to fetch orders'}), 500
        
        return jsonify(orders)
    
    @app.route('/api/customerorders', methods=['POST'])
    def create_customer_order():
        """
        Создание нового заказа покупателя
        """
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        access_token = auth_header.replace('Bearer ', '')
        client = MoyskladClient(access_token)
        
        order_data = request.json
        
        if not order_data:
            return jsonify({'error': 'No order data provided'}), 400
        
        result = client.create_customer_order(order_data)
        
        if result is None:
            return jsonify({'error': 'Failed to create order'}), 500
        
        return jsonify(result)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )