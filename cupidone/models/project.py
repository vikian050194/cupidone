from typing import List

from cupidone.common import app_name, app_version, legend, card_state_emojies_map, checklist_state_emojies_map
from cupidone.dc import CompiledCard
from cupidone.views.base import AbstractView, ListView
from cupidone.views.message import ErrorView, InfoView

from .base import AbstractModel


class ProjectModel(AbstractModel):
    def initialize_new_project(self):
        self.fm.initialize_new_project()
        self._save_todo(cards=[])

    def build_project(self):
        cards = []
        for key, value in self.fm.get_cards_map().items():
            file_name = self.fm.get_relative_card_name(key)
            card_name = value[0].removeprefix("# ").removesuffix("\n")
            state_name = value[6].removeprefix("State: `").removesuffix("`\n")
            cards.append(CompiledCard(
                file_name=file_name,
                name=card_name,
                state_name=state_name,
                checklist=[],
                checklist_name=None,
                created_at=None,
                desc=None,
                types=[]
            ))
        return self._save_todo(cards=cards)

    def _save_todo(self, cards: List[CompiledCard]) -> AbstractView:
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
        cards_desc_output = []
        if cards:
            for i, card in enumerate(cards):
                if card.state_name not in card_state_emojies_map:
                    return ErrorView(f"unexpected card state - {card.state_name}")
                state_emoji = card_state_emojies_map[card.state_name]
                card_desc = f"{state_emoji} [{card.name}]({card.file_name})"
                cards_desc_output.append(card_desc)
                if i < len(cards) - 1:
                    lines.append(f"{card_desc}\\\n")
                else:
                    lines.append(f"{card_desc}\n")
        else:
            lines.append("empty\n")
        lines.append("\n")
        lines.append(f"<!-- {app_name} v{app_version} -->")
        lines.append("\n")

        self.fm.write_todo(lines)

        if cards:
            return ListView(cards_desc_output)
        else:
            return InfoView("there are no cards yet")

    def add_card(self, card: CompiledCard):
        lines = []
        lines.append(f"# {card.name}\n")
        lines.append("\n")
        lines.append(f"Created at: `{card.created_at}`\n")
        lines.append("\n")
        lines.append(f"Type: ")
        lines.append(", ".join([f'`{t}`' for t in card.types]))
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
                if item.state_name not in checklist_state_emojies_map:
                    return ErrorView(f"unexpected checklist item state - {item.state}")
                state_emoji = checklist_state_emojies_map[item.state_name]
                item_desc = f"{state_emoji} {item.name}"
                if i < len(card.checklist) - 1:
                    lines.append(f"{item_desc}\\\n")
                else:
                    lines.append(f"{item_desc}\n")
        else:
            lines.append("empty\n")

        self.fm.write_card(card.file_name, lines)

    def read_json(self, filename:str):
        return self.fm.read_json(filename)


__all__ = ["ProjectModel"]
