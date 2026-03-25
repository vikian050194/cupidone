# cupidone

[![MIT license][license-badge]][license-url]
[![Maintenance status][status-badge]][status-url]
[![PyPI version][pypi-badge]][pypi-url]
[![Downloads per week][downloads-badge]][downloads-url]
[![Code coverage][coverage-badge]][coverage-url]

## About

**cupidone** is a tool that can help you track progress on tasks and plan future work

## Motivation

There are a lot of flexible and powerful UI-rich task trackers but as for me all of them are too complex and I don't need a biggest part of provided features

## Requirements

Python version 3.9 or higher

Developed and tested on Ubuntu 20.04

<!-- skip-start -->

## Installation

**PyPI**

```
pip3 install cupidone
```

**From sources**

1. Clone the repo
    ```
    git clone https://github.com/vikian050194/cupidone.git
    ```
2. Install the package globally
    ```
    pip3 install .
    ```
3. Call installed package via a generated standalone "shim" script
    ```
    cupidone
    ```
    or run Python module
    ```
    python3 cupidone
    ```

## Development

```
virtualenv venv
source venv/bin/activate
pip install -e .
```

<!-- skip-stop -->

## Usage

In general invocation has following format `cupidone [COMMAND] [SUBCOMMAND] [OPTIONS] [VALUE]`

### Help

Format: `cupidone [COMMAND]`

| Command | Description |
| --- | --- |
| `help` | Help information |
| `version` | Installed version |

### Initialize

Format: `cupidone init`

This command creates `TODO.md` and empty `todo` directory

### Add

Format: `cupidone add`

This command creates new empty card in the `todo` directory

### Build

Format: `cupidone build`

This command (re)builds `TODO.md` according to the cards from `todo` directory

### Dump

Format: `cupidone dump`

This command dump all cards from `todo` directory

### Migrate

To migrate from different sources

Format: `cupidone migrate [OPTION] [VALUE]`

| Option | Description |
| --- | --- |
| `trello` | Trello kanban project as source |
| `vanilla` | Vanilla markdown as source |

One value is required - path to exported `JSON` file

### Configuration

There in one way/layer of configuration

**Environment variables**

| Name | Description | Value |
| --- | --- | --- |
| `PWD` | Project directory where `README.md` file and `todo` directory are stored | Any valid path |
| `CUPIDONE_OUTPUT` | Output format | `human`, `plain` or `json` |

<!-- skip-start -->

## Tests

Module for testing is `unittest`

```
python3 -m unittest discover -t=. -s=tests/ -p=test_*.py
```

or

```
./shell/test.sh
```

### Coverage

Install requrements
```
pip install -r requirements.txt
```

Generate coverage results
```
coverage run -m unittest
```

To get total coverage percent
```
coverage report --format=total
```

To make text report
```
coverage report --format=text
```

To make HTML coverage report run following commands
```
coverage html
```

or

```
./shell/coverage.sh
```

<!-- skip-stop -->

[status-url]: https://github.com/vikian050194/cupidone/pulse
[status-badge]: https://img.shields.io/github/last-commit/vikian050194/cupidone.svg

[license-url]: https://github.com/vikian050194/cupidone/blob/master/LICENSE
[license-badge]: https://img.shields.io/github/license/vikian050194/cupidone.svg

[pypi-url]: https://pypi.org/project/cupidone
[pypi-badge]: https://img.shields.io/pypi/v/cupidone

[downloads-url]: https://pypi.org/project/cupidone
[downloads-badge]: https://img.shields.io/pypi/dw/cupidone

[coverage-url]: https://codecov.io/gh/vikian050194/cupidone
[coverage-badge]: https://img.shields.io/codecov/c/github/vikian050194/cupidone
