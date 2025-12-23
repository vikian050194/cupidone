from cupidone.actions import Commands

from ..composite import CompositeController


class MigrationController(CompositeController):
    def keys(self):
        return [Commands.MIGRATION]


__all__ = ["MigrationController"]