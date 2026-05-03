from typing import List, Optional

from cupidone.common import *
from cupidone.common import dt_to_iso
from cupidone.dc import CompiledCard, CompiledChecklistItem, WebData
from cupidone.views.base import AbstractView, ListView
from cupidone.views.message import ErrorView, InfoView

from .base import AbstractModel


class ProjectModel(AbstractModel):
    def init_project(self) -> AbstractView:
        self.fm.init_project()
        self._save_todo(cards=[])
        return InfoView(f"new project is initialized")

    def _get_value(self, line: str, prefix: str, suffix: str):
            return line.removeprefix(prefix).removesuffix(suffix)

    def _find_value(self, lines: list[str], prefix: str, suffix: str):
        for line in lines:
            if line.startswith(prefix):
                return self._get_value(line, prefix, suffix)
        return None

    def _get_checklist(self, lines: list[str]):
        checklist: list[CompiledChecklistItem] = []
        for line in lines:
            if line.startswith("⚪ "):
                value = self._get_value(line, "⚪ ", "\\\n")
                checklist.append(CompiledChecklistItem(value, ChecklistItemState.INCOMPLETE))
            elif line.startswith("🟢 "):
                value = self._get_value(line, "🟢 ", "\\\n")
                checklist.append(CompiledChecklistItem(value, ChecklistItemState.COMPLETE))
        return checklist

    def _get_description(self, lines: list[str]):
        start_index = None
        end_index = None
        for i, line in enumerate(lines):
            if "Description" in line:
                start_index = i + 1
                continue
            if start_index is not None and "#" in line:
                end_index = i - 1
                break
        description = lines[start_index:end_index]
        description = map(lambda l: l.replace("\n", ""), description)
        return list(description)

    def _list_cards(self) -> list[CompiledCard]:
        cards = []
        for file_name, lines in self.fm.get_cards_map().items():
            id = self._get_card_id(file_name)
            full_file_name = self.fm.get_relative_card_name(file_name)
            card_name = self._find_value(lines, "# ", "\n")
            state_name = self._find_value(lines, "State: `", "`\n")
            created_at = self._find_value(lines, "Created at: `", "`\n")
            types = self._find_value(lines, "Type: ", "\n").split(", ")
            types = map(lambda t: t.removeprefix("`").removesuffix("`"), types)
            types = list(types)
            state = CardState(state_name)
            checklist = self._get_checklist(lines)
            checklist_name = self._find_value(lines, "### ", "\n")
            description = self._get_description(lines)
            cards.append(CompiledCard(
                id=id,
                file_name=full_file_name,
                name=card_name,
                state=state,
                checklist=checklist,
                checklist_name=checklist_name,
                created_at= created_at,
                description=description,
                types=types
            ))
        return cards

    def build_project(self):
        cards = self._list_cards()
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
        if card.description:
            lines.append(f"{card.description}\n")
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

    def _get_card_id(self, file_name: str):
        return int(file_name.removesuffix(".md"))

    def add_empty_card(self):
        files = self.fm.get_cards_map().keys()
        files_list = list(files)
        new_card_id = 1
        file_name = self._get_file_name(1)
        if files_list:
            last_file = files_list[-1]
            last_card_id = self._get_card_id(last_file)
            new_card_id = last_card_id + 1
            file_name = self._get_file_name(new_card_id)
        title = "New card title"
        description = "Card description"
        state=CardState.BACKLOG
        checklist_name = None
        checklist = []
        types = [member.value for member in CardType]
        created_at = dt_to_iso(self.tm.get_datetime())
        empty_card = CompiledCard(
            id=new_card_id,
            file_name=file_name,
            name=title,
            description=description,
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

    def read_lines(self, filename:str):
        return self.fm.read_lines(filename)

    def dump(self):
        cards = self._list_cards()
        return ListView(list=cards)

    def build_site(self, title: Optional[str]):
        build = dt_to_iso(self.tm.get_datetime())
        site_title = title or self.fm.get_project_dir()
        cards = self._list_cards()
        data = WebData(
            build=build,
            title=site_title,
            cards=cards
        )
        self.fm.build_site(data)
        return InfoView("done")

__all__ = ["ProjectModel"]
