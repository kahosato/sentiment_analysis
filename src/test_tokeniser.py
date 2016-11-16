import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src')

from unittest import TestCase

# The two most important rules are to (generally) split on whitespace, and to split punctuation off
# into their own tokens. Other than that, you will need to find an acceptable treatment for mid-word
# alphanumerics (eight-year-old-child), contractions (I'll, don't) and genitives (Paul's).
from tokens import WordToken, PunctuationToken
from tokeniser import Tokeniser


class TestTokeniser(TestCase):
    def test_tokenise_whitespace(self):
        cases = {
            "an    apple.": [WordToken("an"), WordToken("apple"), PunctuationToken(".")],
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_comma(self):
        cases = {
            "I, for one.": [WordToken("i"), PunctuationToken(","), WordToken("for"), WordToken("one"),
                            PunctuationToken(".")]
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_bracket(self):
        cases = {
            "(I, for one.)": [PunctuationToken("("), WordToken("i"), PunctuationToken(","), WordToken("for"),
                              WordToken("one"),
                              PunctuationToken("."), PunctuationToken(")")]
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_hyphen(self):
        # "eight-year-old-child"
        # 8-year-old ? cf tokenise_id
        cases = {
            "eight-year-old child": [WordToken("eight"), PunctuationToken("-"), WordToken("year"),
                                     PunctuationToken("-"), WordToken("old"), WordToken("child")],
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_slash(self):
        # love/hate relationship
        cases = {
            "love/hate relationship": [WordToken("love"), PunctuationToken("/"), WordToken("hate"),
                                       WordToken("relationship")],
            "this love/ hate relationship": [WordToken("this"), WordToken("love"), PunctuationToken("/"),
                                             WordToken("hate"),
                                             WordToken("relationship")],
            "weird-love /hate relationship": [WordToken("weird"), PunctuationToken("-"), WordToken("love"),
                                              PunctuationToken("/"), WordToken("hate"),
                                              WordToken("relationship")],
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_id(self):
        # B456F7-3
        cases = {
            "like B456F7-3": [WordToken("like"), WordToken("B456F7-3")],
            "like B456F7-3-like": [WordToken("like"), WordToken("B456F7-3-like")],
            "8-years-old": [WordToken("8-years-old")],
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_ll(self):
        cases = {
            "I'll": [WordToken("i"), WordToken("will")],
            "Sam'll": [WordToken("sam"), WordToken("will")],
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_i(self):
        cases = {
            "well I think": [WordToken("well"), WordToken("i"), WordToken("think")],
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_nt(self):
        cases = {
            "Don't": [WordToken("do"), WordToken("not")],
            "hasn't": [WordToken("has"), WordToken("not")]
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_s(self):
        # has / genitive / is ambiguous so just leave it as is
        cases = {
            "It's": [WordToken("it"), WordToken("'s")],
            "He's": [WordToken("he"), WordToken("'s")],
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_d(self):
        # he'd -> he had / he would ambiguous, so just leave it
        cases = {
            "It'd": [WordToken("it"), WordToken("'d")],
            "He'd": [WordToken("he"), WordToken("'d")],
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_ve(self):
        # I've -> I have, as there is no ambiguity
        cases = {
            "I've": [WordToken("i"), WordToken("have")],
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_tokenise_capital_middle(self):
        # I thought it was GREAT. -> GREAT should be capitalised
        # I love Paris -> Paris should be capitalised
        # Paris I love -> paris + i + love (I should go lowercase)
        cases = {
            "I thought it was GREAT": [WordToken("i"), WordToken("thought"), WordToken("it"), WordToken("was"),
                                       WordToken("GREAT")],
            "I love Paris": [WordToken("i"), WordToken("love"), WordToken("Paris")],
            "Paris I love": [WordToken("paris"), WordToken("i"), WordToken("love")],
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected

    def test_period(self):
        # Ph.D -> Ph.D
        # U.S.A. -> U.S.A + period if end of sentence, U.S.A if middle
        cases = {
            "I have a Ph.D.": [WordToken("i"), WordToken("have"), WordToken("a"), WordToken("Ph.D"),
                               PunctuationToken(".")],
            "Make U.K. great again.": [WordToken("make"), WordToken("U.K"), PunctuationToken("."), WordToken("great"),
                                       WordToken("again"),
                                       PunctuationToken(".")]
        }
        for input, expected in cases.iteritems():
            assert Tokeniser.tokenise_sentence(input) == expected
