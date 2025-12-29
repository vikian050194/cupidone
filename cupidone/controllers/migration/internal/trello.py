import os

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
            checklist = Checklist(
                id=c["id"],
                name=c["name"],
                checkItems=check_items
            )
            checklists.append(checklist)

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
        types: Set[str] = set()
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
            if action.type not in types:
                types.add(action.type)

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
            file_name = f"{i:04}.md"
            state_name = states_map[card.idState]
            state_emoji = state_emojies_map[state_name]
            # TODO use relative path
            name = card.name
            created_at = created_at[card.id]
            types = [labels_map[idLabel] for idLabel in card.idLabels]
            desc = card.desc
            if len(card.idChecklists) > 1:
                return ErrorView("only one checklist is supported")
            checklist_name = None
            checklist: List[ChecklistItem] = []
            if card.idChecklists:
                checklistFoo = checklists_map[card.idChecklists[0]]
                check_items = checklistFoo.checkItems
                for i, item in enumerate(check_items):
                    state_char = ""
                    if item.state == "incomplete":
                        state_char = "⚪"
                    elif item.state == "complete":
                        state_char = "🟢"
                    else:
                        return ErrorView(f"unexpected state - {item.state}")
                    checklist.append(ChecklistItem(
                        name=item.name,
                        state_name=item.state,
                        state_emoji=state_char
                    ))
            results.append(CompiledCard(
                file_name=file_name,
                name=name,
                desc=desc,
                state_name=state_name,
                state_emoji=state_emoji,
                checklist_name=checklist_name,
                checklist=checklist,
                types=types,
                created_at=created_at
            ))

        return model.build_project()
