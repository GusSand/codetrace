from typing import TypeAlias
__typ0 : TypeAlias = "Logger"
"""manages configuring logging for the app."""

import logging
import logging.handlers
import os
from logging import Logger, StreamHandler
from logging.handlers import RotatingFileHandler
from typing import Union


class LogConfiguration:
    """handle common logging options for the entire project."""

    def __tmp2(__tmp1, __tmp3: str, filename: str, debug: bool = False) -> None:
        # create console handler
        __tmp1._consoleLogger = logging.StreamHandler()
        __tmp1._consoleLogger.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
        if debug:
            __tmp1._consoleLogger.setLevel(logging.DEBUG)
        else:
            __tmp1._consoleLogger.setLevel(logging.INFO)
        # create a file handler
        path = os.path.join(__tmp3, 'logs', f'{filename}.log')
        __tmp1._fileLogger = logging.handlers.RotatingFileHandler(path, maxBytes=1024 * 1024, backupCount=20)
        __tmp1._fileLogger.setLevel(logging.DEBUG)
        # create a logging format
        formatter = logging.Formatter('[%(name)s][%(levelname)s][%(asctime)s] %(message)s')
        __tmp1._fileLogger.setFormatter(formatter)

    @property
    def file_logger(__tmp1) :
        """
        Get file logger.

        :return: file logger
        :rtype: logging.handlers.RotatingFileHandler
        """
        return __tmp1._fileLogger

    @property
    def console_logger(__tmp1) -> StreamHandler:
        """
        Get console logger.

        :return: console logger
        :rtype: logging.StreamHandler
        """
        return __tmp1._consoleLogger

    def __tmp0(__tmp1, name: <FILL>) -> __typ0:
        """
        Create new logger for the app.

        :param name: name for the logger
        :type name: str
        :return: logger
        :rtype: logging.Logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        # add the handlers to the logger
        logger.addHandler(__tmp1.file_logger)
        logger.addHandler(__tmp1.console_logger)

        return logger
