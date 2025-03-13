from logger_helper import LevelFileHandler, ASCIIFilter


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "{levelname} | {name} | {asctime} | {lineno} | {message}",
            "style": "{"
        },
        "format_http": {
            "format": "{levelname} | {name} | {lineno} | {message}",
            "style": "{"
        }
    },
    "filters": {
        "ascii_filter": {
            "()": ASCIIFilter,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": "ext://sys.stdout",
        },
        "handler_http": {
            "class": "logging.handlers.HTTPHandler",
            "formatter": "format_http",
            "level": "DEBUG",
            "host": "127.0.0.1:5000",
            "url": "/log",
            "method": "POST"
        },
        "file": {
            "()": LevelFileHandler,
            "level": "DEBUG",
            "formatter": "base",
            "file_name": "logfile.log",
            "mode": "a"
        }
    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["handler_http", "console"],
        },
        "utils": {
            "level": "DEBUG",
            "filters": ["ascii_filter",],
            "handlers": ["handler_http", "console"],
        },
    },
}