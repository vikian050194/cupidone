from .base import BasePrinter, to_str


class PlainPrinter(BasePrinter):
    def print_str(self, message):
        self.__print__(message.value)

    def print_object(self, object):
        for k, v in object.__dict__.items() :
            self.__print__(f"{k}: {to_str(v)}")

    def print_message(self, message):
        self.__print__(f"{message.level}: {to_str(message.value)}")

    def print_list(self, list):
        self.__print__(" ".join(list))


__all__ = ["PlainPrinter"]
