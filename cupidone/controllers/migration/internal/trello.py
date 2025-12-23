import os
import json

from sys import argv
from typing import Any, Dict, List, Set

from cupidone.dc import *
from cupidone.common import *
from cupidone.actions import MigrationOptions
from cupidone.controllers.abstract import AbstractController
# from cupidone.models.project import ProjectModel
from cupidone.views.base import ListView
from cupidone.views.message import InfoView


class MigrationTrelloController(AbstractController):
    def keys(self):
        return [MigrationOptions.TRELLO]

    def handle(self, options):
        pass
        # model = ProjectModel(self.pm, self.tm)
        # current_project = model.get()
        # if current_project:
        #     return StrView(current_project)
        # else:
        #     return InfoView("current project is not specified")


# def run(source_file_name: str) -> None:
#     with open(source_file_name, "r") as fr:
#         values: Dict[str, Any] = json.load(fr)

#     for k in values:
#         print(k)

#     labels: List[Label] = []
#     for l in values["labels"]:
#         label = Label(
#             id=l["id"],
#             name=l["name"]
#         )
#         labels.append(label)
#         print(label)

#     checklists: List[Checklist] = []
#     for c in values["checklists"]:
#         check_items: List[ChecklistItem] = []
#         for item in c["checkItems"]:
#             checkItem = ChecklistItem(
#                 id=item["id"],
#                 name=item["name"],
#                 state=item["state"]
#             )
#             check_items.append(checkItem)
#         checklist = Checklist(
#             id=c["id"],
#             name=c["name"],
#             checkItems=check_items
#         )
#         checklists.append(checklist)
#         print(checklist)

#     states: List[State] = []
#     for c in values["lists"]:
#         column = State(
#             id=c["id"],
#             name=c["name"]
#         )
#         states.append(column)
#         print(column)

#     cards: List[Card] = []
#     for c in values["cards"]:
#         card = Card(
#             id=c["id"],
#             name=c["name"],
#             desc=c["desc"],
#             idState=c["idList"],
#             idChecklists=c["idChecklists"],
#             idLabels=c["idLabels"]
#         )
#         cards.append(card)
#         print(card)

#     actions: List[Action] = []
#     types: Set[str] = set()
#     for a in values["actions"]:
#         action = Action(
#             id=a["id"],
#             type=a["type"],
#             date=a["date"]
#         )
#         if a["data"].get("card") and a["data"]["card"].get("id"):
#             action.cardId=a["data"]["card"]["id"]
#         if a["data"].get("listBefore") and a["data"].get("listAfter"):
#             action.stateBefore = a["data"]["listBefore"]
#             action.stateAfter = a["data"]["listAfter"]
#         actions.append(action)
#         if action.type not in types:
#             types.add(action.type)
#         print(action)
#     print(types)

#     items = []
#     states_map = {s.id: s.name for s in states}
#     labels_map = {l.id: l.name for l in labels}
#     checklists_map = {c.id: c for c in checklists}

#     created_at = {}
#     for action in actions:
#         if action.type in ["createCard", "copyCard"] and action.cardId not in created_at:
#             created_at[action.cardId] = action.date

#     cards.sort(key=lambda c: created_at[c.id])

#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     for i, card in enumerate(cards, start=1):
#         file_name = f"{output_dir}/{i:04}.md"
#         state_name = states_map[card.idState]
#         state_emoji = state_emojies_map[state_name]
#         item = f"{state_emoji} [{card.name}]({file_name})"
#         items.append(item)
#         with open(file_name, "w") as f:
#             f.write(f"# {card.name}\n")
#             f.write("\n")
#             f.write(f"Created at: `{created_at[card.id]}`\n")
#             f.write("\n")
#             f.write(f"Type: ")
#             f.write(", ".join([f"`{labels_map[idLabel]}`" for idLabel in card.idLabels]))
#             f.write("\n")
#             f.write("\n")
#             f.write(f"State: ")
#             f.write(f"`{states_map[card.idState]}`\n")
#             f.write("\n")
#             f.write(f"## Description\n")
#             if card.desc:
#                 f.write(f"{card.desc}\n")
#             else:
#                 f.write("empty\n")
#             f.write("\n")
#             f.write(f"## Checklist\n")
#             for checklist_id in card.idChecklists:
#                 checklist = checklists_map[checklist_id]
#                 check_items = checklist.checkItems
#                 f.write(f"### {checklist.name}\n")
#                 for i, item in enumerate(check_items):
#                     state_char = ""
#                     if item.state == "incomplete":
#                         state_char = "⚪"
#                     elif item.state == "complete":
#                         state_char = "🟢"
#                     else:
#                         print(f"unexpected state - {item.state}")
#                     if i < len(check_items) - 1:
#                         f.write(f"{state_char} {item.name}\\\n")
#                     else:
#                         f.write(f"{state_char} {item.name}\n")
#             if not card.idChecklists:
#                 f.write("empty\n")

#     with open("TODO.md", "w") as f:
#         f.write("# TODO\n")
#         f.write("\n")
#         f.write("## 🧭 Legend\n")
#         for i, line in enumerate(legend):
#             if i < len(legend) - 1:
#                 f.write(f"{line}\\\n")
#             else:
#                 f.write(f"{line}\n")
#         f.write("\n")
#         f.write("## 📋 Issues\n")
#         for i, item in enumerate(items):
#             if i < len(items) - 1:
#                 f.write(f"{item}\\\n")
#             else:
#                 f.write(f"{item}\n")
        
#         f.write("\n")
#         f.write(f"<!-- {app_name} v{app_version} -->")
#         f.write("\n")

#     for item in items:
#         print(item)
