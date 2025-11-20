import requests
import json
from flask import current_app

class MoyskladClient:
    """Клиент для работы с API МойСклад"""
    
    def __init__(self, access_token=None):
        self.base_url = 'https://api.moysklad.ru/api/remap/1.2'
        self.access_token = access_token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip'
        }
        
        if access_token:
            self.headers['Authorization'] = f'Bearer {access_token}'
    
    def set_access_token(self, access_token):
        """Установить токен доступа"""
        self.access_token = access_token
        self.headers['Authorization'] = f'Bearer {access_token}'
    
    def get_customer_orders(self, limit=100, offset=0):
        """Получить список заказов покупателей"""
        url = f"{self.base_url}/entity/customerorder"
        params = {
            'limit': limit,
            'offset': offset
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error fetching customer orders: {e}")
            return None
    
    def get_customer_order(self, order_id):
        """Получить конкретный заказ покупателя"""
        url = f"{self.base_url}/entity/customerorder/{order_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error fetching customer order {order_id}: {e}")
            return None
    
    def create_customer_order(self, order_data):
        """Создать новый заказ покупателя"""
        url = f"{self.base_url}/entity/customerorder"
        
        try:
            response = requests.post(url, headers=self.headers, json=order_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error creating customer order: {e}")
            return None
    
    def update_customer_order(self, order_id, update_data):
        """Обновить заказ покупателя"""
        url = f"{self.base_url}/entity/customerorder/{order_id}"
        
        try:
            response = requests.put(url, headers=self.headers, json=update_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error updating customer order {order_id}: {e}")
            return None
    
    def get_account_info(self):
        """Получить информацию об аккаунте"""
        url = f"{self.base_url}/context/companySettings"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error fetching account info: {e}")
            return None