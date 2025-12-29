from dataclasses import dataclass
from typing import List, Optional


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


@dataclass
class CompiledChecklistItem():
    name: str
    state_name: str


@dataclass
class CompiledCard():
    file_name: str
    name: str
    desc: str
    state_name: str
    checklist_name: Optional[str]
    checklist: List[CompiledChecklistItem]
    types: List[str]
    created_at: str
