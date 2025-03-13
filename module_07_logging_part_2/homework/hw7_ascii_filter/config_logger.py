from logger_helper import LevelFileHandler, ASCIIFilter


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "{levelname} | {name} | {asctime} | {lineno} | {message}",
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
            "handlers": ["file", "console"],
        },
        "util": {
            "level": "DEBUG",
            "filters": ["ascii_filter",],
            "handlers": ["file", "console"],
        },
    },
}