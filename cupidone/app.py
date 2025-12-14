from sys import argv

from cupidone.main import main


def run():
    options = argv[1:]
    main(options=options)


if __name__ == '__main__':
    run()
