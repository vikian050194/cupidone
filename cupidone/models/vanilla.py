from typing import List

from cupidone.common import CardType, dt_to_iso
from cupidone.dc import *
from cupidone.views.base import AbstractView

from .project import ProjectModel


class VanillaMigrator():
    def __init__(self, pm: ProjectModel):
        self.pm = pm

    def _get_initial_card_state(self, line: str, is_backlog, is_todo):
        if "~" in line:
            return CardState.OUTDATED
        if line.startswith("- [ ]"):
            if is_todo:
                return CardState.TODO
            if is_backlog:
                return CardState.BACKLOG
        if line.startswith("- [x]"):
            return CardState.DONE
        return None

    def _get_card_name(self, line: str):
        return line.removeprefix("- [ ] ").removeprefix("- [x] ").removeprefix("~").removeprefix("~").removesuffix("~").removesuffix("~")

    def _get_checklist_item_state(self, line: str):
        if line.startswith("  - [ ] "):
            return ChecklistItemState.INCOMPLETE
        if line.startswith("  - [x] "):
            return ChecklistItemState.COMPLETE
        return None

    def _get_checklist_item_name(self, line: str):
        return line.removeprefix("  - [ ] ").removeprefix("  - [x] ").removeprefix("~").removeprefix("~").removesuffix("~").removesuffix("~")

    def get_compiled_cards(self, filename: str):
        lines = self.pm.read_lines(filename)
        is_todo = False
        is_backlog = False
        index = 1
        result: List[CompiledCard] = []
        for line in lines:
            if line == "# TODO":
                continue
            if line == "":
                continue
            if line == "empty":
                continue
            if line == "## Backlog":
                is_todo = False
                is_backlog = True
                continue
            if line == "## Todo":
                is_todo = True
                is_backlog = False
                continue
            if line.startswith("  - ["):
                checklist_item = CompiledChecklistItem(
                    name=self._get_checklist_item_name(line),
                    state=self._get_checklist_item_state(line)
                )
                result[-1].checklist.append(checklist_item)
                if checklist_item.state == ChecklistItemState.COMPLETE and result[-1].state in [CardState.TODO, CardState.BACKLOG]:
                    result[-1].state = CardState.INPROGRESS
                continue
            cc_file_name = f"{index:04}.md"
            cc_state = self._get_initial_card_state(line, is_backlog, is_todo)
            cc_name = self._get_card_name(line)
            cc_created_at = dt_to_iso(self.pm.tm.get_datetime())
            cc_types = [ct.value for ct in CardType]
            cc_desc = cc_name
            cc_checklist_name = "Empty checklist name"
            cc_checklist: List[ChecklistItem] = []
            result.append(CompiledCard(
                id=index,
                file_name=cc_file_name,
                name=cc_name,
                description=cc_desc,
                state=cc_state,
                checklist_name=cc_checklist_name,
                checklist=cc_checklist,
                types=cc_types,
                created_at=cc_created_at
            ))
            index += 1
        return result

    def migrate(self, filename: str) -> AbstractView:
        cards = self.get_compiled_cards(filename)

        self.pm.init_project()

        for card in cards:
            self.pm.add_card(card)

        return self.pm.build_project()


__all__ = ["VanillaMigrator"]
