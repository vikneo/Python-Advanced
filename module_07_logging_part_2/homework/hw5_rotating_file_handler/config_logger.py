import os

filename = os.path.join(os.path.dirname(__file__), "utils.log")

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "{levelname} | {name} | {asctime} | {lineno} | {message}",
            "style": "{"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "base",
            "filename": filename,
            "when": "h",
            "interval": 10,
            "backupCount": 5,
            "encoding": "UTF-8"
        }
    },
    "loggers": {
        # "app": {
        #     "level": "DEBUG",
        #     "handlers": ["console",],
        # },
        "util": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
        },
    },
}