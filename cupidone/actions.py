import enum


@enum.unique
class Commands(str, enum.Enum):
    INIT = "init"
    BUILD = "build"
    MIGRATION = "migration"
    HELP = "help"
    VERSION = "version"


@enum.unique
class MigrationOptions(str, enum.Enum):
    TRELLO = "trello"
