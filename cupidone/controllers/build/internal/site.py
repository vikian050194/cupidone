from cupidone.dc import *
from cupidone.common import *
from cupidone.actions import BuildOptions
from cupidone.controllers.abstract import AbstractController
from cupidone.models.project import ProjectModel
from cupidone.views.base import AbstractView


class BuildSiteController(AbstractController):
    def keys(self):
        return [BuildOptions.SITE]

    def handle(self, options) -> AbstractView:
        pm = ProjectModel(self.fm, self.tm)
        title = None
        if options.values:
            title = options.values[0]
        return pm.build_site(title)
