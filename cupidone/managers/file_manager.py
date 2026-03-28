import abc
import json
import os
import re

from datetime import datetime
from pkgutil import get_data

from typing import Any, Dict, List

from cupidone.card import Card
from cupidone.configuration import Configuration
from cupidone.dc import WebData
from cupidone.printers.json import EnhancedJSONEncoder

from .time_manager import AbstractTimeManager


def to_action(data):
    type = data.get("type")
    value = data.get("value")
    timestamp = datetime.fromisoformat(data.get("timestamp"))
    return Card(type, timestamp, value)


class AbstractFileManager(abc.ABC):
    @abc.abstractmethod
    def init_project(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_cards_map(self) -> Dict[str, List[str]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def write_card(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def write_todo(self, lines: List[str]) -> None:
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
        self._site_dir = "site"
        self._templates_dir = "templates"
        self._site_data_json = "data.json"
        self._toc_file_name = "TODO.md"

    def init_project(self):
        if not os.path.exists(self._full_cards_dir_path):
            os.makedirs(self._full_cards_dir_path)

    def write_card(self, filename:str, lines: List[str]):
        with open(self._get_full_card_path(filename), "w") as fw:
            fw.writelines(lines)

    def write_todo(self, lines: List[str]):
        with open(self._full_todo_path, "w") as fw:
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

    def read_lines(self, filename: str):
        with open(filename, "r") as fr:
            return fr.read().splitlines()

    # TODO rename function
    def get_project_dir(self):
        return self._project_dir.split(os.sep)[-1]

    def build_site(self, data: WebData):
        data_json = json.dumps(data, sort_keys=True, indent=4, cls=EnhancedJSONEncoder)
        full_site_dir = os.path.join(self._project_dir, self._site_dir)
        if not os.path.exists(full_site_dir):
            os.makedirs(full_site_dir)
        full_data_json = os.path.join(full_site_dir, self._site_data_json)
        with open(full_data_json, "w") as fw:
            fw.writelines(data_json)

        # TODO copy all files from templates to site via one call
        # shutil.copyfile(src=os.path.join(full_site_dir, "index.html"), dst=os.path.join(full_site_dir, "index.html"))
        # shutil.copyfile(src=os.path.join(full_site_dir, "index.js"), dst=os.path.join(full_site_dir, "index.js"))
        # shutil.copyfile(src=os.path.join(full_site_dir, "index.css"), dst=os.path.join(full_site_dir, "index.css"))
        # shutil.copyfile(src=os.path.join(full_site_dir, "favicon.svg"), dst=os.path.join(full_site_dir, "favicon.svg"))

        # z = zipimporter.get_filename(fullname="cupidone.templates.index.html")

        files = ["index.html", "index.js", "index.css", "favicon.svg"]
        for file in files:
            b = get_data("cupidone", os.path.join(self._templates_dir, file))
            with open(os.path.join(full_site_dir, file), "wb") as fw:
                fw.write(b)

        # import importlib
        # with importlib.resources.path("cupidone.templates", "index.html") as fspath:
        #     result = fspath.stat()
        #     print(result)

__all__ = ["FileManager"]
