import logging
import os


class LevelFileHandler(logging.Handler):

    def __init__(self, file_name, mode="a") -> None:
        super().__init__()
        self.file_name = file_name
        self.mode = mode

    def __created_file(self, file_name: str) -> str:
        """Generate a path for the created file in the current directory"""

        current_dir = os.path.dirname(__file__)
        return os.path.join(current_dir, file_name)

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        level = record.levelname.lower()
        self.file_name = self.__created_file(f"{record.name}_{level}.log")

        with open(self.file_name, self.mode) as file:
            file.write(f"{msg}\n")
