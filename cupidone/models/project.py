from typing import List

from cupidone.common import app_name, app_version, legend, state_emojies_map
from cupidone.dc import CompiledCard
from cupidone.views.base import AbstractView, ListView
from cupidone.views.message import ErrorView, InfoView

from .base import AbstractModel


class ProjectModel(AbstractModel):
    def initialize_new_project(self):
        self.fm.initialize_new_project()
        self._save_todo(items=[])

    def build_project(self):
        items = []
        for key, value in self.fm.get_cards_map().items():
            file_name = self.fm.get_relative_card_name(key)
            card_name = value[0].removeprefix("# ").removesuffix("\n")
            state_name = value[6].removeprefix("State: `").removesuffix("`\n")
            state_emoji = state_emojies_map[state_name]
            item = f"{state_emoji} [{card_name}]({file_name})"
            items.append(item)
        return self._save_todo(items)

    def _save_todo(self, items: List[str]) -> AbstractView:
        lines = []
        lines.append("# TODO\n")
        lines.append("\n")
        lines.append("## 🧭 Legend\n")
        for i, line in enumerate(legend):
            if i < len(legend) - 1:
                lines.append(f"{line}\\\n")
            else:
                lines.append(f"{line}\n")
        lines.append("\n")
        lines.append("## 📋 Issues\n")
        if items:
            for i, item in enumerate(items):
                if i < len(items) - 1:
                    lines.append(f"{item}\\\n")
                else:
                    lines.append(f"{item}\n")
        else:
            lines.append("empty\n")
        lines.append("\n")
        lines.append(f"<!-- {app_name} v{app_version} -->")
        lines.append("\n")

        self.fm.write_todo(lines)

        if items:
            return ListView(items)
        else:
            return InfoView("there are no cards yet")

    def add_card(self, card: CompiledCard):
        lines = []
        lines.append(f"# {card.name}\n")
        lines.append("\n")
        lines.append(f"Created at: `{card.created_at}`\n")
        lines.append("\n")
        lines.append(f"Type: ")
        lines.append(", ".join(card.types))
        lines.append("\n")
        lines.append("\n")
        lines.append(f"State: ")
        lines.append(f"`{card.state_name}`\n")
        lines.append("\n")
        lines.append(f"## Description\n")
        if card.desc:
            lines.append(f"{card.desc}\n")
        else:
            lines.append("empty\n")
        lines.append("\n")
        lines.append(f"## Checklist\n")
        if card.checklist:
            lines.append(f"### {card.checklist_name}\n")
            for i, item in enumerate(card.checklist):
                if i < len(card.checklist) - 1:
                    lines.append(f"{item.state_emoji} {item.name}\\\n")
                else:
                    lines.append(f"{item.state_emoji} {item.name}\n")
        else:
            lines.append("empty\n")

        self.fm.write_card(card.file_name, lines)

    def read_json(self, filename:str):
        return self.fm.read_json(filename)


__all__ = ["ProjectModel"]
