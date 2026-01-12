from typing import List

from cupidone.actions import Commands
from cupidone.controllers.abstract import AbstractController
from cupidone.options import Options
from cupidone.views.base import AbstractView, ListView


class HelpController(AbstractController):
    def keys(self) -> List[str]:
        return [Commands.HELP]

    def handle(self, options: Options) -> AbstractView:
        lines = []
        lines.append((Commands.INIT.value, "to init new project"))
        lines.append((Commands.ADD.value, "to add new empty card"))
        lines.append((Commands.BUILD.value, "to build TODO.md"))
        lines.append((Commands.MIGRATION.value, "to migrate items"))
        lines.append((Commands.VERSION.value, "get version"))
        lines.append((Commands.HELP.value, "get help"))
        return ListView(lines)


__all__ = ["HelpController"]
