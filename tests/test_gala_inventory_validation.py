import unittest

from scripts.gala_inventory_validation import (
    _calendar_indices,
    _paired_statistic,
    _permutation_p_difference,
)


class GalaInventoryValidationTests(unittest.TestCase):
    def test_paired_statistic_keeps_missing_hours_missing(self):
        value, count = _paired_statistic([0.1, None, 0.3, 0.4], [-1.0, 9.0, -3.0, -4.0])
        self.assertEqual(count, 3)
        self.assertAlmostEqual(value, -1.0)

    def test_calendar_indices_are_reproducible_and_bounded(self):
        import random

        first = _calendar_indices(48, random.Random(7))
        second = _calendar_indices(48, random.Random(7))
        self.assertEqual(first, second)
        self.assertEqual(len(first), 48)
        self.assertTrue(all(0 <= value < 48 for value in first))

    def test_difference_permutation_is_deterministic(self):
        control = [0.1] * 48
        event = [0.9] * 48
        first = _permutation_p_difference(control, event, 199, 11)
        second = _permutation_p_difference(control, event, 199, 11)
        self.assertEqual(first, second)
        self.assertIsNotNone(first)


if __name__ == "__main__":
    unittest.main()
