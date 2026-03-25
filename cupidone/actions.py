import enum


@enum.unique
class Commands(str, enum.Enum):
    INIT = "init"
    ADD = "add"
    BUILD = "build"
    MIGRATE = "migrate"
    DUMP = "dump"
    HELP = "help"
    VERSION = "version"


@enum.unique
class MigrationOptions(str, enum.Enum):
    TRELLO = "trello"
    VANILLA = "vanilla"
