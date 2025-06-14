"""
pip install structlog[dev]
"""

import structlog, logging

# Настройка structlog
structlog.configure(
    processors=[
        structlog.processors.add_log_level,  # Добавляет уровень логирования
        structlog.processors.TimeStamper(fmt="iso"),  # Добавляет время
        structlog.dev.ConsoleRenderer(),  # Красивый вывод в консоль
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),  # Уровень логирования
)

logger = structlog.get_logger()

# Примеры логов
logger.debug("Это сообщение не выведется (уровень INFO)")
logger.info("Привет, structlog!", user="Alice", action="login")
logger.warning("Что-то пошло не так", reason="timeout")
logger.error("Ошибка соединения", server="api.example.com", status_code=500)