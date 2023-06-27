import logging
import uuid
from logging.config import dictConfig


class Logger(logging.Logger):
    def __init__(self, name, execution_id=None):
        super().__init__(name)
        color_formatter = ColorFormatter()
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(color_formatter)
        self.addHandler(console_handler)
        self._execution_id = uuid.uuid4() if execution_id is None else execution_id

    def info(self, message, **kwargs):
        super().info(msg=message, extra={"execution_id": self._execution_id})

    def error(self, message, **kwargs):
        super().error(msg=message, extra={"execution_id": self._execution_id})

    def warning(self, message, **kwargs):
        super().warning(msg=message, extra={"execution_id": self._execution_id})

    def debug(self, message, **kwargs):
        super().debug(msg=message, extra={"execution_id": self._execution_id})

    def set_execution_id(self, execution_id):
        self._execution_id = execution_id

    def get_execution_id(self):
        return self._execution_id


class FlaskLogger(Logger):
    def __init__(self, app, name):
        self.name = name
        super().__init__(name)
        self._app = app

    def info(self, message, **kwargs):
        self._app.logger.info(message, **kwargs)

    def error(self, message, **kwargs):
        self._app.logger.error(message, **kwargs)

    def warning(self, message, **kwargs):
        self._app.logger.warning(message, **kwargs)

    def debug(self, message, **kwargs):
        self._app.logger.debug(message, **kwargs)

    def setLevel(self, level) -> None:
        self._app.logger.level = level


import logging


class ExecutionIdFormatter(logging.Formatter):
    def format(self, record):
        if hasattr(record, "execution_id"):
            self._style._fmt = "%(asctime)s - %(name)s - %(levelname)s - %(execution_id)s - %(message)s"
        else:
            self._style._fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        return super().format(record)


class ColorFormatter(logging.Formatter):
    grey = "\x1b[90;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;20m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + "%(asctime)s - %(name)s - %(levelname)s - %(execution_id)s - %(message)s" + reset,
        logging.INFO: green + "%(asctime)s - %(name)s - %(levelname)s - %(execution_id)s - %(message)s " + reset,
        logging.WARNING: yellow + "%(asctime)s - %(name)s - %(levelname)s - %(execution_id)s - %(message)s" + reset,
        logging.ERROR: red + "%(asctime)s - %(name)s - %(levelname)s - %(execution_id)s - %(message)s" + reset,
        logging.CRITICAL: bold_red + "%(asctime)s - %(name)s - %(levelname)s - %(execution_id)s - %(message)s" + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class ExecutionIdAndColorFormatter(logging.Formatter):
    # Define a dictionary of format strings for different log levels
    FORMATS = {
        logging.DEBUG: "\x1b[90;20m%(asctime)s - %(name)s - %(levelname)s - %(execution_id)s - %(message)s\x1b[0m",
        logging.INFO: "\x1b[32;20m%(asctime)s - %(name)s - %(levelname)s - %(execution_id)s - %(message)s\x1b[0m",
        logging.WARNING: "\x1b[33;20m%(asctime)s - %(name)s - %(levelname)s - %(execution_id)s - %(message)s\x1b[0m",
        logging.ERROR: "\x1b[31;20m%(asctime)s - %(name)s - %(levelname)s - %(execution_id)s - %(message)s\x1b[0m",
        logging.CRITICAL: "\x1b[31;1m%(asctime)s - %(name)s - %(levelname)s - %(execution_id)s - %(message)s\x1b[0m"
    }

    def format(self, record):
        if not hasattr(record, "execution_id"):
            record.execution_id = "No Execution ID"
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def set_logging_config(level=logging.INFO):
    logging.config.dictConfig(get_log_configuration(level))


def get_logger_level_by_name(level_name):
    if level_name == "DEBUG":
        return 10
    elif level_name == "INFO":
        return 20
    elif level_name == "WARNING":
        return 30
    elif level_name == "ERROR":
        return 40
    elif level_name == "CRITICAL":
        return 50
    else:
        raise ValueError(f"Invalid log level: {level_name}")

def get_log_configuration(level=logging.INFO):
    return {
        'version': 1,
        'formatters': {'custom': {
            '()': ExecutionIdAndColorFormatter
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'custom'
        }},
        'root': {
            'level': level,
            'handlers': ['wsgi']
        }
    }