class SortedAssociativeArray:
    __slots__ = ['data']

    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def __bool__(self):
        return bool(self.data)

    def index(self, key):
        for i, el in enumerate(self.data):
            if el[0] == key:
                return i
        return -1

    def contains(self, key):
        return -1 != self.index(key)

    def delete(self, key):
        if self.contains(key):
            del self.data[self.index(key)]

    def set(self, key, value):
        self.delete(key)
        self.data.append((key, value))
        self.data = sorted(self.data)

    def get(self, key):
        idx = self.index(key)
        if idx == -1:
            raise KeyError(f"No element {key}")
        return self.data[idx][1]

    def slice(self, key, count):
        idx = self.index(key)
        if idx == -1:
            raise KeyError(f"Can't access unavailable key {key}")
        if count > 0:
            return self.data[idx:idx+count]
        return self.data[idx+count+1:idx+1]

    def shrink(self, size):
        self.data = self.data[-size:]
