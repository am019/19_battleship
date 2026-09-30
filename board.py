class Board:
    SIZE = 6

    def __init__(self):
        self.ships = []
        self.shots = set()

    def in_bounds(self, pos):
        return 0 <= pos[0] < self.SIZE and 0 <= pos[1] < self.SIZE

    def place_ship(self, cells):
        cells = set(cells)
        if not all(self.in_bounds(c) for c in cells):
            raise ValueError("Ship outside board")
        if any(cells & ship for ship in self.ships):
            raise ValueError("Ships overlap")
        self.ships.append(cells)

    def fire(self, pos):
        if not self.in_bounds(pos):
            return "invalid"
        if pos in self.shots:
            return "repeat"
        self.shots.add(pos)
        for ship in self.ships:
            if pos in ship:
                return "sunk" if ship <= self.shots else "hit"
        return "miss"

    def remaining(self):
        return sum(len(ship - self.shots) for ship in self.ships)

    def all_sunk(self):
        return bool(self.ships) and all(ship <= self.shots for ship in self.ships)