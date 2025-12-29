import abc
import json
import os
import re

from datetime import datetime
from typing import Any, Dict, List

from cupidone.card import Card
from cupidone.configuration import Configuration

from .time_manager import AbstractTimeManager


def to_action(data):
    type = data.get("type")
    value = data.get("value")
    timestamp = datetime.fromisoformat(data.get("timestamp"))
    return Card(type, timestamp, value)


class AbstractFileManager(abc.ABC):
    @abc.abstractmethod
    def initialize_new_project(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_cards_map(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def write_card(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def write_todo(self, lines: List[str]):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_relative_card_name(self, key:str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def read_json(self, filename:str) -> Dict[str, Any]:
        raise NotImplementedError()


class FileManager(AbstractFileManager):
    def __init__(self, tm: AbstractTimeManager, configuration: Configuration):
        self.tm = tm
        self._project_dir = configuration.directory
        self._cards_dir = "todo"
        self._toc_file_name = "TODO.md"

    def initialize_new_project(self):
        if not os.path.exists(self._full_cards_dir_path):
            os.makedirs(self._full_cards_dir_path)

    def write_card(self, filename:str, lines: List[str]):
        with open(os.path.join(self._get_full_card_path(filename)), "w") as fw:
            fw.writelines(lines)

    def write_todo(self, lines: List[str]):
        with open(os.path.join(self._full_todo_path), "w") as fw:
            fw.writelines(lines)

    def get_relative_card_name(self, key: str):
        return os.path.join(self._cards_dir, key)

    @property
    def _full_cards_dir_path(self):
        return os.path.join(self._project_dir, self._cards_dir)

    def _get_full_card_path(self, filename:str):
        return os.path.join(self._project_dir, self._cards_dir, filename)

    @property
    def _full_todo_path(self):
        return os.path.join(self._project_dir, self._toc_file_name)

    def get_cards_map(self):
        # TODO use list instead of dict to keep order
        files = os.listdir(self._full_cards_dir_path)
        files = filter(lambda x: re.fullmatch(pattern="\d{4}\.md", string=x), files)
        files = sorted(files)
        values: Dict[str, List[str]] = dict()
        for file in files:
            relative_file_name = os.path.join(self._full_cards_dir_path, file)
            with open(relative_file_name, "r") as fr:
                values[file] = fr.readlines()
        return values

    def read_json(self, filename: str) -> Dict[str, Any]:
        with open(filename, "r") as fr:
            return json.load(fr)


__all__ = ["FileManager"]
