from cupidone.dc import *
from cupidone.common import *
from cupidone.actions import SiteOptions
from cupidone.controllers.abstract import AbstractController
from cupidone.models.project import ProjectModel
from cupidone.views.base import AbstractView


class SiteBuildController(AbstractController):
    def keys(self):
        return [SiteOptions.BUILD]

    def handle(self, options) -> AbstractView:
        pm = ProjectModel(self.fm, self.tm)
        return pm.build_site()
