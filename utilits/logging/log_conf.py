dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "{levelname} | {name} | {asctime} | {lineno} | {message}",
            "style": "{"
        },
        "module_12": {
            'format': '%(threadName)s - %(message)s'
        },
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
        },
        "file_module_12": {
            "class": 'logging.handlers.RotatingFileHandler',
            "level": "INFO",
            "formatter": "module_12",
            "filename": "server.log",
            "mode": "a"
        }
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["file", "console"],
        },
        "star_wars_v2": {
            "level": "WARNING",
            "handlers": ["file"],
        },
        'module_12_server': {
            'level': 'INFO',
            "handlers": ["file_module_12"],
        }
    },
}