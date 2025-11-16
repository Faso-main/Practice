import asyncio
import logging

from maxapi import Bot, Dispatcher, F
from maxapi.types import MessageCreated

logging.basicConfig(level=logging.INFO)

bot = Bot('token________________________________')  
dp = Dispatcher()

@dp.message_created(F.message.body.text)
async def echo(event: MessageCreated):
    sender = event.message.sender
    logging.info(f"Sender object: {sender}")
    text = event.message.body.text if event.message.body else None
    
    if sender is not None:
        user_id = getattr(sender, 'pk', None) or getattr(sender, 'user_id', None) or str(sender)
    else:
        user_id = "unknown"
    
    logging.info(f"Получено сообщение от {user_id}: {text}")
    
    if text:
        await event.message.answer(f"Повторяю за вами: {text}")
        logging.info("Ответ отправлен")
    else:
        logging.warning("Сообщение не содержит текста")


async def main():
    logging.info("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt: logging.info('Остановлено в ручную')
    except Exception as e: logging.warning(f'Ошибка вида: {e}')