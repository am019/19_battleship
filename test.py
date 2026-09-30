import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from board import Board
from ai import AI
from game import Battleship


def play(inputs):
    game = Battleship()
    buf = io.StringIO()
    with patch("builtins.input", side_effect=inputs), redirect_stdout(buf):
        game.run()
    return buf.getvalue()


class BoardTests(unittest.TestCase):
    def setUp(self):
        self.b = Board()
        self.b.place_ship({(0, 0), (0, 1)})
        self.b.place_ship({(3, 3)})

    def test_hit_and_miss(self):
        self.assertEqual(self.b.fire((0, 0)), "hit")
        self.assertEqual(self.b.fire((5, 5)), "miss")

    def test_repeat(self):
        self.b.fire((0, 0))
        self.assertEqual(self.b.fire((0, 0)), "repeat")

    def test_sink_one_then_all(self):
        self.b.fire((0, 0))
        self.assertEqual(self.b.fire((0, 1)), "sunk")
        self.assertFalse(self.b.all_sunk())
        self.assertEqual(self.b.fire((3, 3)), "sunk")
        self.assertTrue(self.b.all_sunk())

    def test_invalid(self):
        self.assertEqual(self.b.fire((6, 0)), "invalid")
        self.assertEqual(self.b.fire((-1, 0)), "invalid")


class AITests(unittest.TestCase):
    def test_never_repeats_and_exhausts(self):
        ai = AI(6)
        shots = [ai.choose() for _ in range(36)]
        self.assertEqual(len(set(shots)), 36)
        self.assertIsNone(ai.choose())

    def test_adjacent_after_hit(self):
        ai = AI(6)
        ai.tried.add((3, 3))
        ai.record((3, 3), "hit")
        self.assertIn(ai.choose(), {(2, 3), (4, 3), (3, 2), (3, 4)})

    def test_corner_hit_stays_in_bounds(self):
        ai = AI(6)
        ai.tried.add((0, 0))
        ai.record((0, 0), "hit")
        self.assertEqual(set(ai.targets), {(1, 0), (0, 1)})

    def test_sunk_clears_targets(self):
        ai = AI(6)
        ai.record((3, 3), "hit")
        ai.record((3, 4), "sunk")
        self.assertEqual(ai.targets, [])

    def test_skips_tried_targets(self):
        ai = AI(6)
        ai.targets = [(1, 1)]
        ai.tried.add((1, 1))
        self.assertNotEqual(ai.choose(), (1, 1))


class GameTests(unittest.TestCase):
    def test_known_ship_cell_is_hit(self):
        out = play(["3,3", "q"])
        self.assertIn("You fired at 3,3: HIT!", out)

    def test_known_empty_cell_is_miss(self):
        out = play(["6,6", "q"])
        self.assertIn("You fired at 6,6: MISS!", out)

    def test_repeat_shot_rejected(self):
        out = play(["3,3", "3,3", "q"])
        self.assertIn("Already fired there.", out)

    def test_invalid_inputs(self):
        out = play(["0,0", "7,1", "abc", "1,2,3", "q"])
        self.assertEqual(out.count("Outside board."), 2)
        self.assertEqual(out.count("Use row,col."), 2)

    def test_quit(self):
        self.assertIn("Goodbye.", play(["q"]))

    def test_sink_all_wins(self):
        cells = ["3,3", "3,4", "3,5", "1,1", "2,1", "5,5", "6,5"]
        out = play(cells)
        self.assertIn("You sank the fleet.", out)
        self.assertIn("Ship sunk!", out)

    def test_one_report_per_shot(self):
        out = play(["3,3", "q"])
        self.assertEqual(out.count("You fired at"), 1)
        self.assertEqual(out.count("AI fired at"), 1)


if __name__ == "__main__":
    unittest.main()