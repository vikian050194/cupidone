from typing import List

from cupidone.controllers.composite import CompositeController
from cupidone.controllers.build import BuildController
from cupidone.controllers.migration import *
from cupidone.controllers.version import VersionController
from cupidone.controllers.help import HelpController
from cupidone.managers import ProjectManager, TimeManager, OutputManager
from cupidone.configuration import Configuration
from cupidone.options import Options


def main(options: List[str], configuration: Configuration):
    tm = TimeManager()
    pm = ProjectManager(tm, configuration)
    om = OutputManager(configuration)

    # TODO improve defaults mechanism
    defaults = dict()

    build_controller = BuildController(pm, tm)

    # TODO move internal controllers inside MigrationController
    migration_subs = [
        MigrationTrelloController(pm, tm)
    ]
    migration_controller = MigrationController(pm, tm, migration_subs)

    version_controller = VersionController(pm, tm)

    help_controller = HelpController(pm, tm)

    controllers = [
        build_controller,
        migration_controller,
        version_controller,
        help_controller
    ]

    root_controller = CompositeController(pm, tm, controllers)

    command = None
    
    if len(options) > 0:
        command = options[0]

    opt = Options(values=options, complete=False)

    if command == "complete":
        command = options[1] if len(options) > 1 else None
        opt = Options(values=options[1:], complete=True)
    else:
        if len(opt.values) < 2 and command in defaults:
            opt.values.append(defaults.get(command))
    view = root_controller.handle(opt)
    om.emmit(view)
