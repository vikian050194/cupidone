import enum


@enum.unique
class Commands(str, enum.Enum):
    INIT = "init"
    ADD = "add"
    BUILD = "build"
    MIGRATION = "migration"
    DUMP = "dump"
    HELP = "help"
    VERSION = "version"


@enum.unique
class MigrationOptions(str, enum.Enum):
    TRELLO = "trello"
