import logging
import logging.handlers

from utils.common import create_subfolders


def setup_logger(log_path):
    logger = logging.getLogger("orix-poc-logger")

    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    create_subfolders(log_path)
    file_handler = logging.FileHandler(log_path)

    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - line: %(lineno)d - %(message)s", datefmt=datefmt
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
