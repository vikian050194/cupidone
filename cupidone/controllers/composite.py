from typing import List

from cupidone.controllers.abstract import AbstractController
from cupidone.controllers.base import BaseController
from cupidone.managers.file_manager import FileManager
from cupidone.managers.time_manager import TimeManager
from cupidone.options import Options
from cupidone.views.base import AbstractView, ListView
from cupidone.views.message import ErrorView


class CompositeController(BaseController):
    def __init__(self, fm: FileManager, tm: TimeManager, cs: List[AbstractController]):
        super().__init__(fm, tm, cs)
        self.handlers = {}
        for c in cs:
            for key in c.keys():
                self.handlers[key] = c

    def keys(self):
        return self.handlers.keys()

    def _complete(self, command: str, args: List[str]) -> AbstractView:
        suggestions = []

        if command:
            if command in self.handlers:
                return self.handlers[command].handle(Options(args, True))

            for key in self.handlers.keys():
                # TODO fix enum and string mixed usage
                if str(key.value).startswith(command):
                    suggestions.append(key.value)

        if suggestions:
            return ListView(suggestions)

        for key in self.handlers.keys():
            # TODO fix enum and string mixed usage
            suggestions.append(key.value)
        return ListView(suggestions)

    def _handle(self, command: str, args: List[str]) -> AbstractView:
        if command in self.handlers:
            # TODO extract options instance
            return self.handlers[command].handle(Options(args, False))
        
        if command:
            return ErrorView(f'command "{command}" is not found, please try "help"')

        return ErrorView(f'command is missed, please try "help"')

    def handle(self, options: Options):
        command = None
        args = []

        if len(options.values) > 0:
            command = options.values[0]

        if len(options.values) > 1:
            args = options.values[1:]

        if options.complete:
            return self._complete(command=command, args=args)

        return self._handle(command=command, args=args)


__all__ = ["CompositeController"]
