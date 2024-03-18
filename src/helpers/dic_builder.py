class DictBuilder:
    def __init__(self):
        self._dict = {}

    def add(self, key, value):
        self._dict[key] = value
        return self

    def build(self):
        return self._dict