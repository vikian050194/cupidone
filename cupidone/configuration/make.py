from pathlib import Path

from cupidone.configuration.output import OutputFlagValues
from cupidone.configuration import Configuration


def make_config(**kwargs):
    config = Configuration()
    
    config._directory = kwargs.get("directory")

    output = OutputFlagValues.HUMAN.value
    config._output = kwargs.get("output") or output

    return config
