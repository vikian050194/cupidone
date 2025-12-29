import abc

from cupidone.managers import FileManager, TimeManager


class AbstractModel(abc.ABC):
    def __init__(self, fm: FileManager, tm: TimeManager):
        self.fm = fm
        self.tm = tm


__all__ = ["AbstractModel"]
