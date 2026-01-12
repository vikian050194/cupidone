from typing import List

from cupidone.controllers import *
from cupidone.managers import *
from cupidone.configuration import Configuration
from cupidone.options import Options


def main(options: List[str], configuration: Configuration):
    tm = TimeManager()
    fm = FileManager(tm, configuration)
    om = OutputManager(configuration)

    # TODO improve defaults mechanism
    defaults = dict()

    init_controller = InitController(fm, tm)
    add_controller = AddController(fm, tm)
    build_controller = BuildController(fm, tm)
    migration_controller = MigrationController(fm, tm)
    version_controller = VersionController(fm, tm)
    help_controller = HelpController(fm, tm)

    controllers = [
        init_controller,
        add_controller,
        build_controller,
        migration_controller,
        version_controller,
        help_controller
    ]

    root_controller = CompositeController(fm, tm, controllers)

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
