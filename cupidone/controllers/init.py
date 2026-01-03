
from typing import List

from cupidone.actions import Commands
from cupidone.controllers.abstract import AbstractController
from cupidone.models.project import ProjectModel
from cupidone.options import Options
from cupidone.views.base import AbstractView
from cupidone.dc import *
from cupidone.common import *


class InitController(AbstractController):
    def keys(self) -> List[str]:
        return [Commands.INIT]

    def handle(self, options: Options) -> AbstractView:
        model = ProjectModel(self.fm, self.tm)
        return model.init_project()


__all__ = ["InitController"]
