__all__ = ['Result']


class Result:
    def __init__(self):
        self.path = None
        raise NotImplementedError

    @property
    def path(self):
        return self.path

    @path.setter
    def path(self, value):
        self._path = value
