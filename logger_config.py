import logging
from colorama import Fore, Style, init
from settings import settings


# Инициализация colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.GREEN,
        logging.INFO: Fore.LIGHTGREEN_EX,
        logging.WARNING: Fore.LIGHTYELLOW_EX,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    @staticmethod
    def give_spase(text: str, spase: int):

        text_len = len(text)
        if text_len > spase:
            return text
        else:
            count_to_add_space = spase - text_len
            return text + " " * count_to_add_space

    def format(self, record):
        # Форматируем asctime
        asctime = self.formatTime(record, self.datefmt)
        path_link = f"{record.pathname}:{record.lineno}"
        record.module = f"{Fore.LIGHTBLACK_EX}{record.module}{Style.RESET_ALL}"
        where = f"{Fore.LIGHTBLACK_EX}in {record.module}{Fore.LIGHTBLACK_EX}.py > {Fore.LIGHTBLACK_EX}{record.funcName}"
        # Окрашиваем levelname и msg
        if record.levelno in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelno]}{self.give_spase(record.levelname, 8)}"
            )
            record.msg = f"{self.COLORS[record.levelno]}{record.msg}{Style.RESET_ALL}"

        log_message = (
            f"\n"
            f"{path_link} {where} - {asctime} - {record.name}\n"
            f"{record.levelname} - {record.msg}"
        )
        return log_message


# Настраиваем цветной вывод в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter())


logger = logging.getLogger("promed-service")

logger.setLevel(settings.LOG_LEVEL)
logger.addHandler(console_handler)
