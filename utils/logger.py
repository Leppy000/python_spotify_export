import json
import logging
from datetime import datetime, UTC
from inspect import getframeinfo, stack

APPLICATION_NAME = "SPOTIFY_EXPORTER"
LOG_LEVEL = "INFO"


class Logger:
    severities = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
        logging.NOTSET: "NOTSET",
    }

    def __init__(
        self,
        log_level: str = LOG_LEVEL,
        application_name: str = APPLICATION_NAME,
        service: str = "excel_generator",
        **kwargs,
    ):
        logger = self.__logger_setup(log_level, application_name)
        self.loggers = {
            logging.CRITICAL: logger.critical,
            logging.ERROR: logger.error,
            logging.WARNING: logger.warning,
            logging.INFO: logger.info,
            logging.DEBUG: logger.debug,
        }
        self.json_message = {
            "timestamp": datetime.now(UTC).isoformat(),
            "applicationName": application_name,
            "service": service,
        }
        if kwargs:
            self.json_message.update(**kwargs)

    def __logger_setup(self, log_level: str, application_name: str):
        logging.basicConfig(level=log_level)
        logger = logging.getLogger(application_name)
        if logger.handlers:
            for handler in logger.handlers:
                logger.removeHandler(handler)
        logger.setLevel(log_level)
        return logger

    def log(self, level, message, **kwargs):
        json_message = self.json_message.copy()
        json_message.update(**kwargs)
        json_message["level"] = level
        json_message["severity"] = self.severities[level]

        caller = getframeinfo(stack()[2][0])
        json_message["message"] = f"[{caller.filename}: {caller.lineno}] {message}"
        exc_info = True if level in (logging.CRITICAL, logging.ERROR) else False
        self.loggers[level](
            json.dumps(json_message, sort_keys=True, default=str), exc_info=exc_info
        )

    def debug(self, message, **kwargs):
        self.log(logging.DEBUG, message, **kwargs)

    def info(self, message, **kwargs):
        self.log(logging.INFO, message, **kwargs)

    def warning(self, message, **kwargs):
        self.log(logging.WARNING, message, **kwargs)

    def error(self, message, **kwargs):
        self.log(logging.ERROR, message, **kwargs)

    def critical(self, message, **kwargs):
        self.log(logging.CRITICAL, message, **kwargs)


logger = Logger()
