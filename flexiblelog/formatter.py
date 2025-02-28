import logging
import inspect
from typing import Any

from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)


class ColourFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.GREEN,
        logging.INFO: Fore.LIGHTGREEN_EX,
        logging.WARNING: Fore.LIGHTYELLOW_EX,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def __init__(self, use_pid: bool = False, datefmt=None):
        super().__init__(datefmt=datefmt)
        self.use_pid = use_pid

    def format(self, record: logging.LogRecord) -> str:
        """
        Форматирует лог-запись с использованием цветов.
        """

        asctime = self.formatTime(record, self.datefmt)
        path_link = f"{record.pathname}:{record.lineno}"
        args = self._get_args(record)
        where = f"{Fore.LIGHTBLACK_EX}in {record.module}{Fore.LIGHTBLACK_EX}.py > {record.funcName}({args})"
        pid = f"{record.processName} - {record.process} | " if self.use_pid else ''

        # Окрашиваем levelname и msg
        if record.levelno in self.COLORS:
            record.levelname = self._colorize_level(record.levelname, record.levelno)
            record.msg = self._colorize_message(record.msg, record.levelno)

        # Формируем основное сообщение
        log_message = (
            f"{path_link} {where} - {asctime}\n"
            f"{pid}{record.levelname} {record.msg}"
        )

        # Добавляем traceback, если есть exc_info
        if record.exc_info:
            log_message += self._format_exception(record.exc_info)

        return log_message

    def _colorize_level(self, levelname: str, levelno: int) -> str:
        """
        Окрашивает уровень логирования.
        """
        color = self.COLORS.get(levelno, "")
        return f"{color}{self._give_space(levelname, 8)}"

    def _colorize_message(self, message: str, levelno: int) -> str:
        """
        Окрашивает сообщение лога.
        """
        color = self.COLORS.get(levelno, "")
        return f"{color}{message}{Style.RESET_ALL}"

    def _format_exception(self, exc_info) -> str:
        """
        Форматирует и окрашивает traceback.
        """
        exc_text = self.formatException(exc_info)
        return f"\n{Fore.RED}{exc_text}{Style.RESET_ALL}"

    def _get_args(self, record: logging.LogRecord) -> str:
        """
        Получает аргументы функции, которая вызвала логгер.
        """
        frame = inspect.currentframe()
        try:
            while frame:
                if frame.f_code.co_name == record.funcName:
                    args, _, _, values = inspect.getargvalues(frame)
                    if args:
                        args = {arg: values[arg] for arg in args}

                        full_args_length = getattr(record, "full_args_length", False)

                        # Форматируем аргументы с использованием генератора
                        formatted_args = (
                            f"{key}: {value}" if full_args_length else f"{key}: {self.truncate(value)}"
                            for key, value in args.items()
                        )

                        # Объединяем результаты в строку
                        return ', '.join(formatted_args)
                    return ''  # чтобы не возвращать None
                frame = frame.f_back
        finally:
            del frame

    @staticmethod
    def truncate(obj: Any) -> str:
        """Принимает результат метода repr"""
        text_repr = repr(obj)
        if len(text_repr) < 70:
            return f"{text_repr}"
        return f"{text_repr[:20].strip()} ... {text_repr[-10:]}"

    @staticmethod
    def _give_space(text: str, space: int) -> str:
        """
        Добавляет пробелы к тексту, чтобы выровнять его.
        """
        text_len = len(text)
        if text_len > space:
            return text
        return text + ":" + " " * (space - text_len)
