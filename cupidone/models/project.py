from typing import List

from cupidone.common import *
from cupidone.common import dt_to_iso
from cupidone.dc import CompiledCard
from cupidone.views.base import AbstractView, ListView
from cupidone.views.message import ErrorView, InfoView

from .base import AbstractModel


class ProjectModel(AbstractModel):
    def init_project(self) -> AbstractView:
        self.fm.init_project()
        self._save_todo(cards=[])
        return InfoView(f"new project is initialized")

    def build_project(self):
        cards = []
        for key, value in self.fm.get_cards_map().items():
            file_name = self.fm.get_relative_card_name(key)
            card_name = value[0].removeprefix("# ").removesuffix("\n")
            state_name = value[6].removeprefix("State: `").removesuffix("`\n")
            state = CardState(state_name)
            cards.append(CompiledCard(
                file_name=file_name,
                name=card_name,
                state=state,
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
        for i, member in enumerate(CardState):
            emoji = card_state_emojies_map[member]
            value = member.value
            if i < len(CardState) - 1:
                lines.append(f"{emoji} - {value}\\\n")
            else:
                lines.append(f"{emoji} - {value}\n")
        lines.append("\n")
        lines.append("## 📋 Issues\n")
        cards_desc_output = []
        if cards:
            for i, card in enumerate(cards):
                state_emoji = card_state_emojies_map[card.state]
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
        lines.append("Type: " + ", ".join([f'`{t}`' for t in card.types]) + "\n")
        lines.append("\n")
        lines.append(f"State: `{card.state.value}`\n")
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
                state_emoji = checklist_state_emojies_map[item.state]
                item_desc = f"{state_emoji} {item.name}"
                if i < len(card.checklist) - 1:
                    lines.append(f"{item_desc}\\\n")
                else:
                    lines.append(f"{item_desc}\n")
        else:
            lines.append("empty\n")

        self.fm.write_card(card.file_name, lines)
        return InfoView("success")

    def _get_file_name(self, card_id: int) -> str:
        return f"{card_id:04d}.md"

    def add_empty_card(self):
        files = self.fm.get_cards_map().keys()
        files_list = list(files)
        file_name = self._get_file_name(1)
        if files_list:
            last_file = files_list[-1]
            last_card_id = int(last_file.removesuffix(".md"))
            file_name = self._get_file_name(last_card_id+1)
        name = "New card title"
        desc = "Card description"
        state=CardState.BACKLOG
        checklist_name = None
        checklist = []
        types = [member.value for member in CardType]
        created_at = dt_to_iso(self.tm.get_datetime())
        empty_card = CompiledCard(
            file_name=file_name,
            name=name,
            desc=desc,
            state=state,
            checklist_name=checklist_name,
            checklist=checklist,
            types=types,
            created_at=created_at
        )
        self.add_card(empty_card)
        return InfoView(f"{file_name} was added")

    def read_json(self, filename:str):
        return self.fm.read_json(filename)


__all__ = ["ProjectModel"]
