import os
from unittest import TestCase

from symbolic import LexiconEntry, LexiconGenerator


class TestLexiconGenerator(TestCase):
    def test_generate(self):
        lex = LexiconGenerator.generate(os.path.abspath("../resources/sent_lexicon"))
        # 0: type=weaksubj len=1 word1=abandoned pos1=adj stemmed1=n priorpolarity=negative
        assert lex["abandoned"] == LexiconEntry(True, 1, "abandoned", "adj", False, False)
        # 32: type=strongsubj len=1 word1=abomination pos1=noun stemmed1=n priorpolarity=negative
        assert lex["abomination"] == LexiconEntry(False, 1, "abomination", "noun", False, False)
        # 240 type=strongsubj len=1 word1=agreeable pos1=anypos stemmed1=y priorpolarity=positive
        assert lex["agreeable"] == LexiconEntry(False, 1, "agreeable", "anypos", True, True)