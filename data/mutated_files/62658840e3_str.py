"""Utils."""
import datetime
import logging
import logging.handlers
import time


get_current_time = lambda: time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


def __tmp0(__tmp1: <FILL>, console_level=logging.INFO, file_level=logging.INFO):
    """Initialize logging module.

    :param log_file_path: Path of the log file.
    :type log_file_path: str.
    """
    prefix_format = '[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s'
    date_format = '%Y %b %d %H:%M:%S'
    rotation_time = datetime.time(hour=4)
    logging.basicConfig(
        level=console_level,
        format=prefix_format,
        datefmt=date_format,
    )
    file_hanfler = logging.handlers.TimedRotatingFileHandler(
        filename=__tmp1,
        when='midnight',
        interval=1,
        backupCount=10,
        atTime=rotation_time
    )
    file_hanfler.setLevel(file_level)
    formatter = logging.Formatter(fmt=prefix_format, datefmt=date_format)
    file_hanfler.setFormatter(formatter)
    logging.getLogger(name=None).addHandler(file_hanfler)
    logging.info("Start ....")
