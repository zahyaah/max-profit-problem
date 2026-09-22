import os
import subprocess
import sys
import unittest

from max_profit import BUILDINGS, NAMES, format_result, max_profit

# Path to the script, so the CLI tests work from any folder
SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "max_profit.py")


def run_cli(*args):
    return subprocess.run(
        [sys.executable, SCRIPT, *args], capture_output=True, text=True
    )


def brute_force(n):
    # Try every possible build order and remember the best money for each (T, P, C) mix
    results = {}

    def build_next(time_used, money, counts):
        mix = tuple(counts)
        results[mix] = max(results.get(mix, 0), money)

        for index, name in enumerate(NAMES):
            finish = time_used + BUILDINGS[name]["build_time"]
            # Only build it if it finishes before time runs out
            if finish < n:
                new_counts = list(counts)
                new_counts[index] += 1
                earned = BUILDINGS[name]["earning"] * (n - finish)
                build_next(finish, money + earned, new_counts)

    build_next(0, 0, [0, 0, 0])

    top = max(results.values())
    best_mixes = [mix for mix in results if results[mix] == top]
    return top, sorted(best_mixes, reverse=True)


class GivenTestCases(unittest.TestCase):
    def test_case_1(self):
        self.assertEqual(max_profit(7), (3000, [(1, 0, 0), (0, 1, 0)]))

    def test_case_2(self):
        self.assertEqual(max_profit(8), (4500, [(1, 0, 0)]))

    def test_case_3(self):
        self.assertEqual(max_profit(13), (16500, [(2, 0, 0)]))


class EdgeCases(unittest.TestCase):
    def test_no_time(self):
        self.assertEqual(max_profit(0), (0, [(0, 0, 0)]))

    def test_nothing_can_finish(self):
        for n in range(1, 5):
            self.assertEqual(max_profit(n), (0, [(0, 0, 0)]))

    def test_only_pub_finishes(self):
        # Pub is done at 4 and earns 1 unit, Theatre is done at 5 and earns nothing
        self.assertEqual(max_profit(5), (1000, [(0, 1, 0)]))

    def test_pub_beats_theatre(self):
        # Pub earns 2 x 1000 = 2000, Theatre earns 1 x 1500 = 1500
        self.assertEqual(max_profit(6), (2000, [(0, 1, 0)]))

    def test_tie_between_theatre_and_two_pubs(self):
        # Theatre earns 4 x 1500 = 6000, two Pubs earn 5 x 1000 + 1 x 1000 = 6000
        self.assertEqual(max_profit(9), (6000, [(1, 0, 0), (0, 2, 0)]))

    def test_theatre_then_pub(self):
        # Theatre earns 6 x 1500 = 9000, then Pub earns 2 x 1000 = 2000
        self.assertEqual(max_profit(11), (11000, [(1, 1, 0)]))

    def test_negative_time(self):
        with self.assertRaises(ValueError):
            max_profit(-1)

    def test_large_input(self):
        self.assertEqual(max_profit(100000), (1499925001000, [(19999, 1, 0)]))


class CompareWithBruteForce(unittest.TestCase):
    def test_small_inputs(self):
        for n in range(0, 36):
            self.assertEqual(max_profit(n), brute_force(n), f"n = {n}")


class GeneralChecks(unittest.TestCase):
    def test_more_time_never_earns_less(self):
        previous = 0
        for n in range(0, 300):
            earnings = max_profit(n)[0]
            self.assertGreaterEqual(earnings, previous)
            previous = earnings

    def test_commercial_park_never_wins(self):
        # Two Theatres take the same 10 units and always earn more
        for n in range(0, 300):
            for mix in max_profit(n)[1]:
                self.assertEqual(mix[2], 0, f"n = {n}")


class Output(unittest.TestCase):
    def test_format(self):
        expected = "Time Unit: 7\nEarnings: $3000\nSolutions\n1. T: 1 P: 0 C: 0\n2. T: 0 P: 1 C: 0"
        self.assertEqual(format_result(7, 3000, [(1, 0, 0), (0, 1, 0)]), expected)

    def test_cli(self):
        result = run_cli("8")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "Time Unit: 8\nEarnings: $4500\nSolutions\n1. T: 1 P: 0 C: 0\n")

    def test_cli_bad_input(self):
        for args in [["-3"], ["abc"], ["2.5"], []]:
            result = run_cli(*args)
            self.assertEqual(result.returncode, 1, f"args = {args}")
            self.assertIn("Usage", result.stdout)


if __name__ == "__main__":
    unittest.main()
