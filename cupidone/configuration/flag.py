import enum


class Flag():
    def __init__(self, short_name: str, full_name: str, values: enum.Enum):
        self._values = values
        self._short_name = short_name
        self._full_name = full_name

    @property
    def short_name(self):
        return self._short_name

    @property
    def full_name(self):
        return self._full_name
