class Configuration():
    def __init__(self):
        self._directory: str = None
        self._output: str = None

    @property
    def directory(self):
        return self._directory

    @property
    def output(self):
        return self._output
