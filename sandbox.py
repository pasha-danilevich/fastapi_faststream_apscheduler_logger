import logging

# Настройка логгера
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Добавление обработчика
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(user_id)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Логирование с дополнительным полем
logger.info("message")