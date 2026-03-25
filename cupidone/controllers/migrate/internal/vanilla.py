from cupidone.dc import *
from cupidone.common import *
from cupidone.actions import MigrationOptions
from cupidone.controllers.abstract import AbstractController
from cupidone.models.project import ProjectModel
from cupidone.models.vanilla import VanillaMigrator
from cupidone.views.base import AbstractView


class MigrationVanillaController(AbstractController):
    def keys(self):
        return [MigrationOptions.VANILLA]

    def handle(self, options) -> AbstractView:
        pm = ProjectModel(self.fm, self.tm)
        migrator = VanillaMigrator(pm)
        return migrator.migrate(options.values[0])
