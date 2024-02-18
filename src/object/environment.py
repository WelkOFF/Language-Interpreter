class Environment:
    def __init__(self, outer=None):
        self.store = {}
        self.outer = outer

    def get(self, name):
        obj = self.store.get(name, None)
        if obj is None and self.outer is not None:
            return self.outer.get(name)
        return obj

    def set(self, name, val):
        self.store[name] = val
        return val


def new_environment():
    return Environment()


def new_enclosed_environment(outer):
    env = Environment()
    env.outer = outer
    return env
