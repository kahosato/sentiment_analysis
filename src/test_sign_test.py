from unittest import TestCase

import util
from signtest import compute_significance_two_tails


class TestSignTest(TestCase):
    def test_compute_significance_two_tails(self):
        cases = [
            (5, 22, 0.0169),
            (16, 22, 0.0525),
            (100, 220, 0.2001),
            (300, 640, 0.1231)
        ]
        for success, total, expected in cases:
            assert util.isclose(compute_significance_two_tails(success, total), expected, rel_tol=1e-03)
