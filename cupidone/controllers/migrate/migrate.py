from cupidone.actions import Commands

from ..composite import CompositeController

from .internal import *


class MigrateController(CompositeController):
    def __init__(self, fm, tm):
        cs = [
            MigrationTrelloController(fm, tm),
            MigrationVanillaController(fm, tm)
        ]
        super().__init__(fm, tm, cs)

    def keys(self):
        return [Commands.MIGRATE]


__all__ = ["MigrateController"]