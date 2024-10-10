import unittest
from src.language import BaseTokens

class TestBaseTokens(unittest.TestCase):
    def test_singleton(self):
        caps1 = BaseTokens.Caps
        caps2 = BaseTokens.Caps

        # test that BaseToken is a singleton class
        self.assertEqual(id(caps1), id(caps2))

    def test_ProperCase(self):
        string = "Testcase"
        match = BaseTokens.ProperCase.value.search(string)

        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), 8)

    # TODO: Finish Tests
