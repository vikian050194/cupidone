import os
import re

from sys import argv
from typing import Dict, List

from dc import *
from common import *


def run(source_dir_name: str) -> None:
    files = os.listdir(os.path.join(source_dir_name, output_dir))
    files = filter(lambda x: re.fullmatch(pattern="\d{4}\.md", string=x), files)
    files = sorted(files)
    values: Dict[str, List[str]] = dict()

    for file in files:
        relative_file_name = os.path.join(source_dir_name, output_dir, file)
        with open(relative_file_name, "r") as fr:
            values[file] = fr.readlines()

    for k in values:
        print(k)

    items = []

    for key, value in values.items():
        file_name = os.path.join(output_dir, key)
        card_name = value[0].removeprefix("# ").removesuffix("\n")
        state_name = value[6].removeprefix("State: `").removesuffix("`\n")
        state_emoji = state_emojies_map[state_name]
        item = f"{state_emoji} [{card_name}]({file_name})"
        items.append(item)

    with open(os.path.join(source_dir_name, "TODO.md"), "w") as f:
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
