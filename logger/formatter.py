import logging
from colorama import Fore, Style, init

from logger.record import CustomLogRecord

# Инициализация colorama
init(autoreset=True)


class Formatter(logging.Formatter):
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
            return text + ":" + " " * count_to_add_space

    def format(self, record: CustomLogRecord):

        asctime = self.formatTime(record, self.datefmt)
        path_link = f"{record.pathname}:{record.lineno}"
        args = ', '.join(f'{key}: {value}' for key, value in record.func_args.items())
        where = f"{Fore.LIGHTBLACK_EX}in {record.module}{Fore.LIGHTBLACK_EX}.py > {record.funcName}({args})"
        # Окрашиваем levelname и msg
        if record.levelno in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelno]}{self.give_spase(record.levelname, 8)}"
            )
            record.msg = f"{self.COLORS[record.levelno]}{record.msg}{Style.RESET_ALL}"

        log_message = (
            f"{path_link} {where} - {asctime}\n"
            f"{record.levelname} {record.msg}"
        )
        return log_message
