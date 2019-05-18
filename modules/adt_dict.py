class AssociativeArray:
    def __init__(self):
        self.array = []

    def insert(self, key, value):
        for pair in self.array:
            if pair[0] == key:`
                return 'Duplicate key'
        return self.array.append((key, value))

    def remove(self, key):
        for pair in self.array:
            if pair[0] == key:
                return self.array.remove(pair)
        return 'Pair does not exist'

    def update(self, key, value):
        for pair in self.array:
            if pair[0] == key:
                self.array.remove(pair)
                return self.array.append((key, value))
        return 'Key does not exist'

    def lookup(self, key):
        for pair in self.array:
            if pair[0] == key:
                return pair[1]
        return 'Key does not exist'


if __name__ == "__main__":
    dct = AssociativeArray()
    dct.insert("hotel", (4, 5))
    print(dct)