from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI(Board.SIZE)
        self._setup()

    def _setup(self):
        self.player.place_ship({(1, 1), (1, 2), (1, 3)})
        self.player.place_ship({(3, 0), (4, 0)})
        self.player.place_ship({(4, 3), (4, 4)})
        self.enemy.place_ship({(2, 2), (2, 3), (2, 4)})
        self.enemy.place_ship({(0, 0), (1, 0)})
        self.enemy.place_ship({(4, 4), (5, 4)})

    def show(self):
        print("\nYour shots are coordinates like 2,3. Enter q to quit.")
        print("Enemy ship cells remaining:", self.enemy.remaining())

    def _parse(self, raw):
        parts = raw.split(",")
        if len(parts) != 2:
            print("Use row,col.")
            return None
        try:
            r, c = int(parts[0]), int(parts[1])
        except ValueError:
            print("Use row,col.")
            return None
        pos = (r - 1, c - 1)
        if not self.enemy.in_bounds(pos):
            print("Outside board.")
            return None
        return pos

    def _report(self, who, pos, result):
        coord = f"{pos[0] + 1},{pos[1] + 1}"
        text = {"hit": "HIT!", "miss": "MISS!", "sunk": "HIT! Ship sunk!"}[result]
        print(f"{who} fired at {coord}: {text}")

    def run(self):
        print("Battleship")
        while True:
            self.show()
            try:
                raw = input("> ").strip().lower()
            except EOFError:
                return
            if raw in ("q", "quit"):
                print("Goodbye.")
                return
            pos = self._parse(raw)
            if pos is None:
                continue
            result = self.enemy.fire(pos)
            if result == "repeat":
                print("Already fired there.")
                continue
            self._report("You", pos, result)
            if self.enemy.all_sunk():
                print("You sank the fleet.")
                return

            ai_pos = self.ai.choose()
            if ai_pos is None:
                print("AI has no cells left to fire at.")
                return
            ai_result = self.player.fire(ai_pos)
            self.ai.record(ai_pos, ai_result)
            self._report("AI", ai_pos, ai_result)
            if self.player.all_sunk():
                print("The AI sank your fleet.")
                return
