from typing import List, Set

from cupidone.dc import *
from cupidone.common import *
from cupidone.actions import MigrationOptions
from cupidone.controllers.abstract import AbstractController
from cupidone.models.project import ProjectModel
from cupidone.views.base import AbstractView
from cupidone.views.message import ErrorView


class MigrationTrelloController(AbstractController):
    def keys(self):
        return [MigrationOptions.TRELLO]

    def handle(self, options) -> AbstractView:
        model = ProjectModel(self.fm, self.tm)
        values = model.read_json(options.values[0])

        # TODO extract the following code to separate class
        labels: List[Label] = []
        for l in values["labels"]:
            label = Label(
                id=l["id"],
                name=l["name"]
            )
            labels.append(label)

        checklists: List[Checklist] = []
        for c in values["checklists"]:
            check_items: List[ChecklistItem] = []
            for item in c["checkItems"]:
                checkItem = ChecklistItem(
                    id=item["id"],
                    name=item["name"],
                    state=item["state"]
                )
                check_items.append(checkItem)
            cc_checklist = Checklist(
                id=c["id"],
                name=c["name"],
                checkItems=check_items
            )
            checklists.append(cc_checklist)

        states: List[State] = []
        for c in values["lists"]:
            column = State(
                id=c["id"],
                name=c["name"]
            )
            states.append(column)

        cards: List[Card] = []
        for c in values["cards"]:
            card = Card(
                id=c["id"],
                name=c["name"],
                desc=c["desc"],
                idState=c["idList"],
                idChecklists=c["idChecklists"],
                idLabels=c["idLabels"]
            )
            cards.append(card)

        actions: List[Action] = []
        cc_types: Set[str] = set()
        for a in values["actions"]:
            action = Action(
                id=a["id"],
                type=a["type"],
                date=a["date"]
            )
            if a["data"].get("card") and a["data"]["card"].get("id"):
                action.cardId=a["data"]["card"]["id"]
            if a["data"].get("listBefore") and a["data"].get("listAfter"):
                action.stateBefore = a["data"]["listBefore"]
                action.stateAfter = a["data"]["listAfter"]
            actions.append(action)
            if action.type not in cc_types:
                cc_types.add(action.type)

        states_map = {s.id: s.name for s in states}
        labels_map = {l.id: l.name for l in labels}
        checklists_map = {c.id: c for c in checklists}

        created_at = {}
        for action in actions:
            if action.type in ["createCard", "copyCard"] and action.cardId not in created_at:
                created_at[action.cardId] = action.date

        cards.sort(key=lambda c: created_at[c.id])

        model.initialize_new_project()

        results: List[CompiledCard] = []
        for i, card in enumerate(cards, start=1):
            cc_file_name = f"{i:04}.md"
            cc_state_name = states_map[card.idState]
            cc_name = card.name
            cc_created_at = created_at[card.id]
            cc_types = [labels_map[idLabel] for idLabel in card.idLabels]
            cc_desc = card.desc
            if len(card.idChecklists) > 1:
                return ErrorView(f"only one checklist is supported - {card.name}")
            cc_checklist_name = None
            cc_checklist: List[ChecklistItem] = []
            if card.idChecklists:
                first_checklist = checklists_map[card.idChecklists[0]]
                cc_checklist_name = first_checklist.name
                check_items = first_checklist.checkItems
                for i, item in enumerate(check_items):
                    cc_checklist.append(CompiledChecklistItem(
                        name=item.name,
                        state_name=item.state
                    ))
            results.append(CompiledCard(
                file_name=cc_file_name,
                name=cc_name,
                desc=cc_desc,
                state_name=cc_state_name,
                checklist_name=cc_checklist_name,
                checklist=cc_checklist,
                types=cc_types,
                created_at=cc_created_at
            ))

        for cc in results:
            model.add_card(cc)

        return model.build_project()
