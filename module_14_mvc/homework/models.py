from typing import Any


class Book:

    def __init__(self, id: int, title: str, author: str, views: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.views: int = views

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)
