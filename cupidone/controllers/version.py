from typing import List

from cupidone.controllers.abstract import AbstractController
from cupidone.actions import Commands
from cupidone.options import Options
from cupidone.views.base import AbstractView, StrView


class VersionController(AbstractController):
    def keys(self) -> List[str]:
        return [Commands.VERSION]

    def handle(self, options: Options) -> AbstractView:
        return StrView("v0.3.0")


__all__ = ["VersionController"]
