from cupidone.dc import *
from cupidone.common import *
from cupidone.actions import MigrationOptions
from cupidone.controllers.abstract import AbstractController
from cupidone.models.project import ProjectModel
from cupidone.models.trello import TrelloMigrator
from cupidone.views.base import AbstractView


class MigrationTrelloController(AbstractController):
    def keys(self):
        return [MigrationOptions.TRELLO]

    def handle(self, options) -> AbstractView:
        pm = ProjectModel(self.fm, self.tm)
        migrator = TrelloMigrator(pm)
        return migrator.migrate(options.values[0])
