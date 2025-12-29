from typing import List

from cupidone.controllers.abstract import AbstractController
from cupidone.managers.file_manager import FileManager
from cupidone.managers.time_manager import TimeManager


class BaseController(AbstractController):
    def __init__(self, fm: FileManager, tm: TimeManager, cs: List[AbstractController]):
        super().__init__(fm, tm)
        self.handlers = {}
        for c in cs:
            for key in c.keys():
                self.handlers[key] = c

    def keys(self):
        return self.handlers.keys()


__all__ = ["BaseController"]
