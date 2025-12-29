from typing import List


class AbstractView():
    pass


class StrView(AbstractView):
    def __init__(self, value: str):
        self.value = value


class ListView(AbstractView):
    def __init__(self, list: List[str]):
        self.list = list


__all__ = [
    "AbstractView",
    "StrView",
    "ListView"
]
