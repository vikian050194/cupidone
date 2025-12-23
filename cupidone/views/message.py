from .base import StrView


class MessageView(StrView):
    def __init__(self, level, value):
        super().__init__(value)
        self.level = level


class InfoView(MessageView):
    def __init__(self, value: str):
        super().__init__("INFO", value)


class WarningView(MessageView):
    def __init__(self, value: str):
        super().__init__("WARNING", value)


class ErrorView(MessageView):
    def __init__(self, value: str):
        super().__init__("ERROR", value)


__all__ = [
    "MessageView",
    "InfoView",
    "WarningView",
    "ErrorView"
]
