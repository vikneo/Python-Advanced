import threading
from decorators.decorators import time_tracker


class ComputationalLoad(threading.Thread):

    def __init__(self, number: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.number = number
        self.result = 0

    def run(self):
        self.result = sum(i ** i for i in range(self.number))
        return self.result


@time_tracker
def main():
    task = ComputationalLoad(number=10000)
    task.start()

    task.join()
    try:
        print(f"Result = {task.result}")
    except ValueError as e:
        print(f"Digit really big : {e}")


if __name__ == '__main__':
    main()
