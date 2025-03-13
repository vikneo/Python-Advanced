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
            "class": 'logging.handlers.RotatingFileHandler',
            "level": "INFO",
            "formatter": "base",
            "filename": "logfile.log",
            "mode": "a"
        }
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["file", "console"],
        },
    },
}