from typing import List, Set

from cupidone.dc import *
from cupidone.views.base import AbstractView

from .project import ProjectModel


class VanillaMigrator():
    def __init__(self, pm: ProjectModel):
        self.pm = pm

    def get_compiled_cards(self, filename: str):
        lines = self.pm.read_lines(filename)
        is_backlog = False
        result: List[CompiledCard] = []
        for line in lines:
            if line == "## Backlog":
                is_backlog = True
            if is_backlog:
                pass
            cc_file_name = f"{i:04}.md"
            state_name = states_map[card.idState]
            cc_state = CardState(state_name)
            cc_name = card.name
            cc_created_at = created_at[card.id]
            cc_types = [labels_map[idLabel] for idLabel in card.idLabels]
            cc_desc = card.desc
            cc_checklist_name = "TBD"
            cc_checklist: List[ChecklistItem] = []
            if card.idChecklists:
                first_checklist = checklists_map[card.idChecklists[0]]
                cc_checklist_name = first_checklist.name
                check_items = first_checklist.checkItems
                for i, item in enumerate(check_items):
                    cc_checklist.append(CompiledChecklistItem(
                        name=item.name,
                        state=ChecklistItemState(item.state)
                    ))
            result.append(CompiledCard(
                id=i,
                file_name=cc_file_name,
                name=cc_name,
                description=cc_desc,
                state=cc_state,
                checklist_name=cc_checklist_name,
                checklist=cc_checklist,
                types=cc_types,
                created_at=cc_created_at
            ))
        return result

    def migrate(self, filename: str) -> AbstractView:
        cards = self.get_compiled_cards(filename)

        # self.pm.init_project()

        for card in cards:
            print(card)
            # self.pm.add_card(card)

        # return self.pm.build_project()


__all__ = ["VanillaMigrator"]
