
from cupidone.actions import BuildOptions
from cupidone.controllers.abstract import AbstractController
from cupidone.models.project import ProjectModel
from cupidone.options import Options
from cupidone.views.base import AbstractView
from cupidone.dc import *
from cupidone.common import *


class BuildTodoController(AbstractController):
    def keys(self):
        return [BuildOptions.TODO]

    def handle(self, options: Options) -> AbstractView:
        model = ProjectModel(self.fm, self.tm)
        return model.build_project()


__all__ = ["BuildTodoController"]
