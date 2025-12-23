import enum


@enum.unique
class OutputFlagValues(str, enum.Enum):
    HUMAN = "human"
    PLAIN = "plain"
    JSON = "json"
