import logging


class CustomLogRecord(logging.LogRecord):
    """Кастомный LogRecord с атрибутом func_args"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем кастомный атрибут
        self.func_args = {}

# Фабрика для создания кастомного LogRecord
def custom_log_record_factory(*args, **kwargs):
    return CustomLogRecord(*args, **kwargs)