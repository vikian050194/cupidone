import os
import json

from dataclasses import dataclass
from sys import argv
from typing import Any, Dict, List, Optional, Set


@dataclass
class Label():
    id: str
    name: str


@dataclass
class ChecklistItem():
    id: str
    name: str
    state: str


@dataclass
class Checklist():
    id: str
    name: str
    checkItems: List[ChecklistItem]


@dataclass
class State():
    id: str
    name: str


@dataclass
class Card():
    id: str
    name: str
    desc: str
    idState: str
    idChecklists: List[str]
    idLabels: List[str]


@dataclass
class Action():
    id: str
    type: str
    date: str
    cardId: Optional[str] = None
    stateBefore: Optional[str] = None
    stateAfter: Optional[str] = None


legend = [
    "🔵 - backlog",
    "⚪ - to do",
    "🟡 - in progress",
    "🟢 - done",
    "⭕ - outdated"
]

app_name = "cupidone"
app_version = "0.1.0"


def run(source_file_name: str) -> None:
    with open(source_file_name, "r") as fr:
        values: Dict[str, Any] = json.load(fr)

    for k in values:
        print(k)

    labels: List[Label] = []
    for l in values["labels"]:
        label = Label(
            id=l["id"],
            name=l["name"]
        )
        labels.append(label)
        print(label)

    checklists: List[Checklist] = []
    for c in values["checklists"]:
        checkItems: List[ChecklistItem] = []
        for item in c["checkItems"]:
            checkItem = ChecklistItem(
                id=item["id"],
                name=item["name"],
                state=item["state"]
            )
            checkItems.append(checkItem)
        checklist = Checklist(
            id=c["id"],
            name=c["name"],
            checkItems=checkItems
        )
        checklists.append(checklist)
        print(checklist)

    states: List[State] = []
    for c in values["lists"]:
        column = State(
            id=c["id"],
            name=c["name"]
        )
        states.append(column)
        print(column)

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
        print(card)

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
        print(action)
    print(types)

    items = []
    statesEmojies = {
        "backlog": "🔵",
        "todo": "⚪",
        "in progress": "🟡",
        "done": "🟢",
        "outdated": "⭕"
    }
    statesMap = {s.id: s.name for s in states}
    labelsMap = {l.id: l.name for l in labels}
    checklistsMap = {c.id: c for c in checklists}

    createdAt = {}
    for action in actions:
        if action.type in ["createCard", "copyCard"] and action.cardId not in createdAt:
            createdAt[action.cardId] = action.date

    cards.sort(key=lambda c: createdAt[c.id])

    dir = "todo"
    if not os.path.exists(dir):
        os.makedirs(dir)

    for i, card in enumerate(cards, start=1):
        fileName = f"{dir}/{i:04}.md"
        stateName = statesMap[card.idState]
        stateEmoji = statesEmojies[stateName]
        item = f"{stateEmoji} [{card.name}]({fileName})"
        items.append(item)
        with open(fileName, "w") as f:
            f.write(f"# {card.name}\n")
            f.write("\n")
            f.write(f"Created at: `{createdAt[card.id]}`\n")
            f.write("\n")
            f.write(f"Type: ")
            f.write(", ".join([f"`{labelsMap[idLabel]}`" for idLabel in card.idLabels]))
            f.write("\n")
            f.write("\n")
            f.write(f"State: ")
            f.write(f"`{statesMap[card.idState]}`\n")
            f.write("\n")
            f.write(f"## Description\n")
            if card.desc:
                f.write(f"{card.desc}\n")
            else:
                f.write("empty\n")
            f.write("\n")
            f.write(f"## Checklist\n")
            for checklistId in card.idChecklists:
                checklist = checklistsMap[checklistId]
                checkItems = checklist.checkItems
                f.write(f"### {checklist.name}\n")
                for i, item in enumerate(checkItems):
                    stateChar = ""
                    if item.state == "incomplete":
                        stateChar = "⚪"
                    elif item.state == "complete":
                        stateChar = "🟢"
                    else:
                        print(f"unexpected state - {item.state}")
                    if i < len(checkItems) - 1:
                        f.write(f"{stateChar} {item.name}\\\n")
                    else:
                        f.write(f"{stateChar} {item.name}\n")
            if not card.idChecklists:
                f.write("empty\n")

    with open("TODO.md", "w") as f:
        f.write("# TODO\n")
        f.write("\n")
        f.write("## 🧭 Legend\n")
        for i, line in enumerate(legend):
            if i < len(legend) - 1:
                f.write(f"{line}\\\n")
            else:
                f.write(f"{line}\n")
        f.write("\n")
        f.write("## 📋 Issues\n")
        for i, item in enumerate(items):
            if i < len(items) - 1:
                f.write(f"{item}\\\n")
            else:
                f.write(f"{item}\n")
        
        f.write("\n")
        f.write(f"<!-- {app_name} v{app_version} -->")
        f.write("\n")

    for item in items:
        print(item)


if __name__ == '__main__':
    source = argv[1]
    run(source_file_name=source)
