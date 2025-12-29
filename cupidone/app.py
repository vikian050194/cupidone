from os import environ
from sys import argv

from cupidone.main import main
from cupidone.configuration import make_config


def run():
    directory = environ.get("PWD", None)
    output = environ.get("CUPIDONE_OUTPUT", None)

    configuration = make_config(directory=directory, output=output)

    options = argv[1:]
    main(options=options, configuration=configuration)


if __name__ == '__main__':
    run()
