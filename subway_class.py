class SubwayStation:
    def __init__(self, name):
        self.name = name
        self.lines = []

    def __str__(self):
        return self.name


class SubwayLine:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name