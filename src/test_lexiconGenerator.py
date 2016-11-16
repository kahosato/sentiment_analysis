import os
from unittest import TestCase

from symbolic import LexiconEntry, LexiconGenerator


class TestLexiconGenerator(TestCase):
    def test_generate(self):
        lex = LexiconGenerator.generate(os.path.abspath("../resources/sent_lexicon"))
        # 0: type=weaksubj len=1 word1=abandoned pos1=adj stemmed1=n priorpolarity=negative
        assert lex["abandoned"] == LexiconEntry(0.5, 1, "abandoned", "adj", False, -1)
        # 32: type=strongsubj len=1 word1=abomination pos1=noun stemmed1=n priorpolarity=negative
        assert lex["abomination"] == LexiconEntry(1, 1, "abomination", "noun", False, -1)
        # 240 type=strongsubj len=1 word1=agreeable pos1=anypos stemmed1=y priorpolarity=positive
        assert lex["agreeable"] == LexiconEntry(1, 1, "agreeable", "anypos", True, 1)
        # type=strongsubj len=1 word1=covet pos1=verb stemmed1=y priorpolarity=both
        assert lex["covet"] == LexiconEntry(1, 1, "covet", "verb", True, 0)

