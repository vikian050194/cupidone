app_name = "cupidone"
app_version = "0.2.0"
output_dir = "todo"

legend = [
    "🔵 - backlog",
    "⚪ - to do",
    "🟡 - in progress",
    "🟢 - done",
    "⭕ - outdated"
]

state_emojies_map = {
    "backlog": "🔵",
    "todo": "⚪",
    "in progress": "🟡",
    "done": "🟢",
    "outdated": "⭕"
}


class BaseConverter():
    def __init__(self):
        pass

    def read(filename:str) -> None:
        pass

    def write() -> None:
        pass


__all__ = [
    "app_name",
    "app_version",
    "output_dir",
    "legend",
    "state_emojies_map"
]
