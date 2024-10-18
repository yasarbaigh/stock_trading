import logging
import time
from logging.handlers import RotatingFileHandler
from datetime import  datetime

class LogUtils:
    file_handle = None
    stream_handler = None
    Path = None

    def __init__(self, log_file_path):
        """
        implementing rotating file handler which will keep rotating logs once it reaches max size
        :param log_file_path:
        """

        log_file_path = log_file_path.format(f'{datetime.now():%Y-%m-%d}')
        LogUtils.file_handle = RotatingFileHandler(log_file_path, mode='a', maxBytes=100 * 1024 * 1024, backupCount=10,
                                                   encoding=None, delay=0)
        formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(funcName)s : %(message)s')
        formatter.converter = time.localtime
        LogUtils.file_handle.setFormatter(formatter)

        # consoleFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        LogUtils.stream_handler = logging.StreamHandler()

    @staticmethod
    def return_logger(name):
        """

        :param name:
        :return:
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(LogUtils.file_handle)
        logger.addHandler(LogUtils.stream_handler)
        return logger
