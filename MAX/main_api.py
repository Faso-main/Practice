import requests
import json
import logging
from typing import Optional, Dict, Any

BOT_TOKEN = ''

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MaxBot:
    def __init__(self, token: str):
        self.token = token
        self.base_url = 'https://platform-api.max.ru'
        self.session = requests.Session()
        
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Базовый метод для выполнения запросов к API"""
        url = f"{self.base_url}{endpoint}"
        params = {"access_token": self.token}
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=30)
            elif method.upper() == "POST":
                response = self.session.post(url, params=params, json=data, timeout=30)
            else:
                logger.error(f"Unsupported method: {method}")
                return None
                
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Request error: {e}")
            return None
    
    def get_me(self) -> Optional[Dict]:
        """Получение информации о боте"""
        return self._make_request("GET", "/me")
    
    def send_message(self, chat_id: int, text: str) -> Optional[Dict]:
        """Отправка сообщения в чат"""
        data = {
            "text": text,
            "chat_id": chat_id
        }
        return self._make_request("POST", "/messages", data)
    
    def send_message_to_user(self, user_id: int, text: str) -> Optional[Dict]:
        """Отправка сообщения пользователю"""
        data = {
            "text": text,
            "user_id": user_id
        }
        return self._make_request("POST", "/messages", data)
    
    def get_updates(self, marker: Optional[int] = None, limit: int = 100) -> Optional[Dict]:
        """Получение обновлений через long polling"""
        params = f"?access_token={self.token}&limit={limit}&timeout=30"
        if marker:
            params += f"&marker={marker}"
        
        url = f"{self.base_url}/updates{params}"
        
        try:
            response = self.session.get(url, timeout=35)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Updates error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Updates request error: {e}")
            return None

class BotHandler:
    def __init__(self, bot: MaxBot):
        self.bot = bot
        self.last_marker = None
    
    def process_message(self, message: Dict) -> bool:
        """Обработка входящего сообщения"""
        try:
            # Получаем текст сообщения и отправителя
            text = message.get('body', {}).get('text', '').strip()
            if not text:
                return False
            
            # Получаем информацию об отправителе и чате
            sender = message.get('sender', {})
            recipient = message.get('recipient', {})
            
            user_id = sender.get('user_id')
            chat_id = recipient.get('chat_id')
            
            if not user_id:
                return False
            
            logger.info(f"Received message from user {user_id}: {text}")
            
            # Простой эхо-бот
            response_text = f"Вы написали: {text}"
            
            # Отправляем ответ
            if chat_id:
                self.bot.send_message(chat_id, response_text)
            else:
                self.bot.send_message_to_user(user_id, response_text)
                
            logger.info(f"Sent response to user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return False
    
    def process_update(self, update: Dict) -> bool:
        """Обработка обновления"""
        update_type = update.get('update_type')
        
        if update_type == 'message_created':
            message = update.get('message', {})
            return self.process_message(message)
        elif update_type == 'bot_started':
            # Обработка запуска бота
            user = update.get('user', {})
            user_id = user.get('user_id')
            chat_id = update.get('chat_id')
            
            if user_id:
                welcome_text = "Привет! Я эхо-бот. Напишите мне что-нибудь, и я повторю это."
                if chat_id:
                    self.bot.send_message(chat_id, welcome_text)
                else:
                    self.bot.send_message_to_user(user_id, welcome_text)
                logger.info(f"Sent welcome message to user {user_id}")
                return True
                
        return False
    
    def run(self):
        """Основной цикл бота"""
        logger.info("Starting Max bot...")
        
        # Проверяем подключение
        bot_info = self.bot.get_me()
        if bot_info:
            logger.info(f"Bot started successfully: {bot_info.get('first_name', 'Unknown')}")
        else:
            logger.error("Failed to get bot info. Check token.")
            return
        
        # Основной цикл опроса
        while True:
            try:
                updates_data = self.bot.get_updates(self.last_marker)
                
                if updates_data and 'updates' in updates_data:
                    updates = updates_data['updates']
                    marker = updates_data.get('marker')
                    
                    if marker:
                        self.last_marker = marker
                    
                    if updates:
                        logger.info(f"Received {len(updates)} updates")
                        
                        for update in updates:
                            self.process_update(update)
                    else:
                        logger.debug("No new updates")
                else:
                    logger.warning("No updates data received")
                    
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                import time
                time.sleep(5)  # Пауза перед повторной попыткой

def main():
    # Создаем экземпляр бота
    bot = MaxBot(BOT_TOKEN)
    
    # Создаем обработчик
    handler = BotHandler(bot)
    
    # Запускаем бота
    handler.run()

if __name__ == "__main__":
    main()