import logging
import logging.config
import os
import sys

from pythonjsonlogger import jsonlogger

def setup_logger(settings):
    try:
        os.makedirs(settings.LOG_DIR, exist_ok=True)
    except OSError as e:
        print(f"Critical error: {e}", file=sys.stderr)
        sys.exit(1)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "json": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(levelname)s %(message)s %(module)s %(funcName)s %(lineno)d %(filename)s %(threadName)s %(thread)d %(process)d %(processName)s %(created)s %(relativeCreated)s %(msecs)d %(name)s %(levelno)d %(run)d %(special)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "standard",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "INFO",
                    "formatter": "json",
                    "filename": f"{settings.LOG_DIR}/app.log",
                    "maxBytes": 10 * 1024 * 1024,
                    "backupCount": 5,
                    "encoding": "utf8",
                },
                "error_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "ERROR",
                    "formatter": "json",
                    "filename": f"{settings.LOG_DIR}/error.log",
                    "maxBytes": 10 * 1024 * 1024,
                    "backupCount": 5,
                    "encoding": "utf8",
                },
            },
            "root": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console", "file", "error_file"],
            },
        }
    )