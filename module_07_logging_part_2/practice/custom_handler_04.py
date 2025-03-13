import logging
import sys


class CustomFileHandler(logging.Handler):
    def __init__(self, file_name, mode = 'a'):
        super().__init__()
        self.file_name = file_name
        self.mode = mode

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        with open(self.file_name, mode = self.mode) as f:
            f.write(f"{message}\n")


class CustomStreamHandler(logging.StreamHandler):
    def __init__(self, stream = None):
        super().__init__()

        if stream is None:
            stream = sys.stderr
        self.stream = stream
