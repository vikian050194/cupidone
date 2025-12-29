import json

from .base import BasePrinter, to_str


class JsonPrinter(BasePrinter):
    def print_str(self, message):
        self.print_object(message)

    def __to_dict__(self, object):
        object_dict = object.__dict__
        result_dict = {}
        keys = list(object_dict.keys())
        for key in keys:
            result_dict[key] = to_str(object_dict[key])
        return result_dict

    def print_object(self, object):
        dct = self.__to_dict__(object)
        self.__print__(json.dumps(dct, sort_keys=True, indent=4))

    def print_message(self, message):
        self.print_object(message)

    def print_list(self, list):
        self.__print__(json.dumps(list, sort_keys=True, indent=4))


__all__ = ["JsonPrinter"]
