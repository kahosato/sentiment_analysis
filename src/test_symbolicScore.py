import os
from unittest import TestCase

from symbolic import LexiconGenerator, SymbolicScore
from tokeniser import Tokeniser


class TestSymbolicScore(TestCase):
    def setUp(self):
        self.lexicon = LexiconGenerator.generate(os.path.abspath("../resources/sent_lexicon"))

    def test_compute_binary(self):
        cases = [
            ("agilely agility agitate", 1),
            ("agilely agitated of", 0)
        ]
        for s, expected in cases:
            tokens = Tokeniser.tokenise_sentence(s)
            assert SymbolicScore.compute_binary(tokens, self.lexicon) == expected

    def test_compute_weighted(self):
        cases = [
            ("agilely agility agitate", 0),
            ("agilely agitated of", -0.5)
        ]
        for s, expected in cases:
            tokens = Tokeniser.tokenise_sentence(s)
            assert SymbolicScore.compute_weighted(tokens, self.lexicon) == expected
