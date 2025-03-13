"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""
import sys
import traceback
from types import TracebackType
from typing import Type, Literal, IO


class Redirect:
    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.sys_stdout = sys.stdout
        self.sys_stderr = sys.stderr

    def __enter__(self):
        if self.stdout:
            sys.stdout = self.stdout

        if self.stderr:
            sys.stderr = self.stderr

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        try:
            if exc_type:
                if self.stderr:
                    sys.stderr.write(traceback.format_exc())
                    return True
                return exc_val
        finally:
            if self.stdout:
                sys.stdout = self.sys_stdout
                self.stdout.close()

            if self.stderr:
                sys.stderr = self.sys_stderr
                self.stderr.close()


if __name__ == "__main__":
    file_stdout = open("stdout.txt", "w")
    file_stderr = open("stderr.txt", "w")

    with Redirect(file_stdout, file_stderr):
        print(f"{' ' * 10}Дзен Python\nПростое лучше, чем сложное.")
        raise Exception(f"\n{' ' * 10}Дзен Python Error\nСтоять лучше, чем никогда.")
