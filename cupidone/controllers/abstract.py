import abc
from typing import List

from cupidone.managers import ProjectManager, TimeManager
from cupidone.options import Options
from cupidone.views.base import AbstractView


class AbstractController(abc.ABC):
    def __init__(self, pm: ProjectManager, tm: TimeManager):
        self.pm = pm
        self.tm = tm

    @abc.abstractmethod
    def keys(self) -> List[str]:
        pass

    @abc.abstractmethod
    def handle(self, options: Options) -> AbstractView:
        pass


__all__ = ["AbstractController"]
