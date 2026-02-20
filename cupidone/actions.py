import enum


@enum.unique
class Commands(str, enum.Enum):
    INIT = "init"
    ADD = "add"
    BUILD = "build"
    MIGRATION = "migration"
    DUMP = "dump"
    SITE = "site"
    HELP = "help"
    VERSION = "version"


@enum.unique
class MigrationOptions(str, enum.Enum):
    TRELLO = "trello"


@enum.unique
class SiteOptions(str, enum.Enum):
    BUILD = "build"
