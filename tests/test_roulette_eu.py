#TODO: Add test cases for roulette EU

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from casino.accounts import Account
from casino.config import Config
from casino.types import GameContext
from casino.games.roulette.european_roulette import EuropeanRoulette


class TestRoundResults(unittest.TestCase):
    def setUp(self):
        self.ctx = GameContext(account=Account.generate("TEST", 90), config=Config.default())
        self.roulette = EuropeanRoulette([self.ctx.account])
        self.roulette.bets = {
            str(self.ctx.account.aid): {"type": "outside_color", "value": "red", "amount": 10}
        }
        self.roulette.winning_value = ("32", "red", 0, 16)

    def test_payout_returns_lines(self):
        lines = self.roulette.payout()

        self.assertEqual(self.ctx.account.balance, 110)
        self.assertEqual(lines, [
            "Paying out all winners...",
            "Player 1: Won 20 coins.",
            "Finished payout.",
        ])

    @patch("casino.games.roulette.european_roulette.clear_screen")
    def test_show_round_results_prints_header_once(self, mock_clear):
        lines = self.roulette.payout()
        out = io.StringIO()
        with redirect_stdout(out):
            self.roulette.show_round_results(self.ctx, lines)
        output = out.getvalue()

        mock_clear.assert_called_once()
        self.assertNotIn("\x1b[H", output)
        self.assertEqual(output.count("R O U L E T T E"), 1)
        self.assertIn("110", output)
        self.assertIn("Winning number: 32", output)
        self.assertIn("Player 1: Won 20 coins.", output)


if __name__ == "__main__":
    unittest.main()
