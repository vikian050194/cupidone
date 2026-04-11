from .base import BasePrinter, to_str


class PlainPrinter(BasePrinter):
    def print_str(self, message):
        self._print(message.value)

    def print_object(self, object):
        for k, v in object.__dict__.items() :
            self._print(f"{k}: {to_str(v)}")

    def print_message(self, message):
        self._print(f"{message.level}: {to_str(message.value)}")

    def print_list(self, list):
        self._print(" ".join(list))


__all__ = ["PlainPrinter"]
