from custom_handler_04 import CustomFileHandler, CustomStreamHandler

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": '{levelname} || {name} || {message} || {module}.{funcName}:{lineno} - {very}',
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "()": CustomStreamHandler,
            "level": "DEBUG",
            "formatter": "base",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "()": CustomFileHandler,
            "level": "DEBUG",
            "formatter": "base",
            "file_name": "custom_log_file.log",
            "mode": "a",
            # "class": "logging.handlers.RotatingFileHandler",
            # "level": "DEBUG",
            # "formatter": "base",
            # "maxBytes": 1024 * 1024 * 10,
            # "backupCount": 5,
            # "filename": "practice.log",
            # "mode": "a",
        }
    },
    "loggers": {
        "sub_2": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
        }
    },
}
