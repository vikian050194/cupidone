import json
import dataclasses

from .base import BasePrinter


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class JsonPrinter(BasePrinter):
    def print_str(self, message):
        self.print_object(message)

    def print_object(self, object):
        self._print(json.dumps(object, sort_keys=True, indent=4, cls=EnhancedJSONEncoder))

    def print_message(self, message):
        self.print_object(message)

    def print_list(self, list):
        self._print(json.dumps(list, sort_keys=True, indent=4, cls=EnhancedJSONEncoder))


__all__ = ["JsonPrinter"]
