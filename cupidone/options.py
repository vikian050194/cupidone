from typing import List


class Options():
    def __init__(self, values: List[str], complete: bool):
        self.values = values
        self.complete = complete
