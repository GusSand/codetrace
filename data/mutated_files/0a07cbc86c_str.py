from typing import TypeAlias
__typ0 : TypeAlias = "bool"
# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import logging
import logging.config
import sys
from typing import Optional

FORMATTERS = {
    'verbose': {
        'format': '[%(asctime)s:%(levelname)s:%(name)s:%(funcName)s] %(message)s',
        'datefmt': "%Y-%m-%d:%H:%M:%S",
    },
    'simple': {
        'format': '[%(levelname)s:%(name)s] %(message)s'
    },
}

FILE_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': FORMATTERS,
    'handlers': {
        'rotating': {
            'level': 'INFO',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 10000000,
            'backupCount': 5,
            'filename': 'sockeye.log',
        }
    },
    'root': {
        'handlers': ['rotating'],
        'level': 'DEBUG',
    }
}

CONSOLE_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': FORMATTERS,
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'simple',
            'class': 'logging.StreamHandler',
            'stream': None
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    }
}

FILE_CONSOLE_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': FORMATTERS,
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'simple',
            'class': 'logging.StreamHandler',
            'stream': None
        },
        'rotating': {
            'level': 'INFO',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 10000000,
            'backupCount': 5,
            'filename': 'sockeye.log',
        }
    },
    'root': {
        'handlers': ['console', 'rotating'],
        'level': 'DEBUG',
    }
}

LOGGING_CONFIGS = {
    "file_only": FILE_LOGGING,
    "console_only": CONSOLE_LOGGING,
    "file_console": FILE_CONSOLE_LOGGING,
}


def __tmp0() :
    version = sys.version_info
    return version[0] == 3 and version[1] == 4


def setup_main_logger(name: <FILL>, file_logging=True, console=True, path: Optional[str] = None) :
    """
    Return a logger that configures logging for the main application.

    :param name: Name of the returned logger.
    :param file_logging: Whether to log to a file.
    :param console: Whether to log to the console.
    :param path: Optional path to write logfile to.
    """
    if file_logging and console:
        log_config = LOGGING_CONFIGS["file_console"]
    elif file_logging:
        log_config = LOGGING_CONFIGS["file_only"]
    else:
        log_config = LOGGING_CONFIGS["console_only"]

    if path:
        log_config["handlers"]["rotating"]["filename"] = path  # type: ignore

    logging.config.dictConfig(log_config)
    __tmp2 = logging.getLogger(name)

    def exception_hook(__tmp3, __tmp1, __tmp4):
        if __tmp0():
            # Python3.4 does not seem to handle logger.exception() well
            import traceback
            traceback = "".join(traceback.format_tb(__tmp4)) + __tmp3.name
            __tmp2.error("Uncaught exception\n%s", traceback)
        else:
            __tmp2.exception("Uncaught exception", exc_info=(__tmp3, __tmp1, __tmp4))

    sys.excepthook = exception_hook

    return __tmp2


def log_sockeye_version(__tmp2):
    from sockeye import __version__, __file__
    try:
        from sockeye.git_version import git_hash
    except ImportError:
        git_hash = "unknown"
    __tmp2.info("Sockeye version %s, commit %s, path %s", __version__, git_hash, __file__)


def __tmp5(__tmp2):
    from mxnet import __version__, __file__
    __tmp2.info("MXNet version %s, path %s", __version__, __file__)
