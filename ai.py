import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()
        self.targets = []

    def choose(self):
        pos = None
        while self.targets and pos is None:
            candidate = self.targets.pop(0)
            if candidate not in self.tried:
                pos = candidate
        if pos is None:
            options = [(r, c) for r in range(self.size) for c in range(self.size)
                       if (r, c) not in self.tried]
            if not options:
                return None
            pos = random.choice(options)
        self.tried.add(pos)
        return pos

    def record(self, pos, result):
        if result == "sunk":
            self.targets.clear()
        elif result == "hit":
            r, c = pos
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                n = (r + dr, c + dc)
                if (0 <= n[0] < self.size and 0 <= n[1] < self.size
                        and n not in self.tried and n not in self.targets):
                    self.targets.append(n)