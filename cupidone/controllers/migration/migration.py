from cupidone.actions import Commands

from ..composite import CompositeController

from .internal import *


class MigrationController(CompositeController):
    def __init__(self, fm, tm):
        cs = [
            MigrationTrelloController(fm, tm)
        ]
        super().__init__(fm, tm, cs)

    def keys(self):
        return [Commands.MIGRATION]


__all__ = ["MigrationController"]