from cupidone.actions import Commands

from ..composite import CompositeController

from .internal import *


class BuildController(CompositeController):
    def __init__(self, fm, tm):
        cs = [
            BuildTodoController(fm, tm),
            BuildSiteController(fm, tm)
        ]
        super().__init__(fm, tm, cs)

    def keys(self):
        return [Commands.BUILD]


__all__ = ["BuildController"]