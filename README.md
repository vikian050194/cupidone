# cupidone

[![MIT license][license-badge]][license-url]
[![Maintenance status][status-badge]][status-url]
[![Code coverage][coverage-badge]][coverage-url]

## About

**cupidone** is a tool that can help you track progress on tasks and plan future work

By the way, there is [todo list](./TODO.md).

## Motivation

There are a lot of flexible and powerful UI-rich task trackers but as for me all of them are too complex and I don't need a biggest part of provided features

## Requirements

Python version 3.9 or higher

Developed and tested on Ubuntu 20.04

## Installation

Rigth now the best way to install **cupidone** is following one:
1. Clone the repo
    ```
    git clone https://github.com/vikian050194/cupidone.git
    ```
2. Make directory for custom bash completion scripts and grant full access for everyone (TODO: fix this dirty manual hack)
    ```
    mkdir "$HOME/.bash_completion.d"
    chmod 777 "$HOME/.bash_completion.d"
    ```
3. Install the package globally

   Privileged user is required because bash completion file will be copied to `etc` directory
    ```
    pip3 install .
    ```
4. Call installed package via a generated standalone "shim" script
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

## Usage

In general invocation has following format `cupidone [COMMAND] [SUBCOMMAND] [OPTIONS]`

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

### Migration

To migrate from different sources

Format: `cupidone migration [OPTION] [VALUE]`

| Option | Description |
| --- | --- |
| `trello` | Trello kanban project as source |

One value is required - path to exported `JSON` file

### Configuration

There in one way/layer of configuration

**Environment variables**

| Name | Description | Value |
| --- | --- | --- |
| `PWD` | Project directory where `README.md` file and `todo` directory are stored | Any valid path |
| `CUPIDONE_OUTPUT` | Output format | `human`, `plain` or `json` |

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

[status-url]: https://github.com/vikian050194/cupidone/pulse
[status-badge]: https://img.shields.io/github/last-commit/vikian050194/cupidone.svg

[license-url]: https://github.com/vikian050194/cupidone/blob/master/LICENSE
[license-badge]: https://img.shields.io/github/license/vikian050194/cupidone.svg

[coverage-url]: https://codecov.io/gh/vikian050194/cupidone
[coverage-badge]: https://img.shields.io/codecov/c/github/vikian050194/cupidone
