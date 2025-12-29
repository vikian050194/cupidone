import builtins

from datetime import date, datetime, time, timedelta

from cupidone.views import MessageView
from cupidone.common import date_to_yms, dt_to_iso, time_to_hms, timedelta_to_hms


def to_str(value):
    if type(value) is time:
        return time_to_hms(value)
    if type(value) is timedelta:
        return timedelta_to_hms(value)
    if type(value) is date:
        return date_to_yms(value)
    if type(value) is datetime:
        return dt_to_iso(value)
    return value


class BasePrinter():
    def __print__(self, message):
        builtins.print(message)

    def print_str(self, message: str):
        raise NotImplementedError()

    def print_object(self, object):
        raise NotImplementedError()

    def print_message(self, message: MessageView):
        raise NotImplementedError()

    def print_list(self, list):
        raise NotImplementedError()


__all__ = ["BasePrinter"]
