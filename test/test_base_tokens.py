import unittest
from src.language import BaseTokens

class TestBaseTokens(unittest.TestCase):
    def test_singleton(self):
        caps1 = BaseTokens.Caps
        caps2 = BaseTokens.Caps

        # test that BaseToken is a singleton class
        self.assertEqual(id(caps1), id(caps2))

    def test_ProperCase_Pos(self):
        string = "Testcase"
        match = BaseTokens.ProperCase.value.search(string)

        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), 8)

    def test_ProperCase_Neg(self):
        string = "testcase"
        match = BaseTokens.ProperCase.value.search(string)

        self.assertEqual(match, None)

    def test_Caps_Pos(self):
        string = "Testcase"
        match = BaseTokens.Caps.value.search(string)

        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), 1)

    def test_Caps_Pos(self):
        string = "testcase"
        match = BaseTokens.Caps.value.search(string)

        self.assertEqual(match, None)

    def test_LowerCase_Pos(self):
        string = "Testcase"
        match = BaseTokens.LowerCase.value.search(string)

        self.assertEqual(match.start(), 1)
        self.assertEqual(match.end(), 8)

    def test_LowerCase_Twice(self):
        string = "test case"
        matches = BaseTokens.LowerCase.value.findall(string)

        self.assertEqual(len(matches), 2)

    def test_Digits(self):
        string = "testcase1"
        match = BaseTokens.Digits.value.search(string)

        self.assertEqual(match.start(), 8)
        self.assertEqual(match.end(), 9)

        string = "123abc456"
        matches = BaseTokens.Digits.value.findall(string)

        self.assertEqual(len(matches), 2)

    def test_Alphabets(self):
        string = "TestCase"
        match = BaseTokens.Alphabets.value.search(string)

        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(string))

        string = "Test Case"
        matches = BaseTokens.Alphabets.value.findall(string)

        self.assertEqual(len(matches), 2)

    def test_Alphanumeric(self):
        string = "TestCase1"
        match = BaseTokens.Alphanumeric.value.search(string)

        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(string))

    def test_Whitespace(self):
        string = "Test Case 1"
        match = BaseTokens.Whitespace.value.search(string)

        self.assertEqual(match.start(), 4)
        self.assertEqual(match.end(), 5)

        matches = BaseTokens.Whitespace.value.findall(string)

        self.assertEqual(len(matches), 2)

        string = "Test          Case"
        match = BaseTokens.Whitespace.value.findall(string)

        self.assertEqual(len(match), 1)

    def test_StartT(self):
        string = "Test Case"
        match = BaseTokens.StartT.value.search(string)
        matches = BaseTokens.StartT.value.findall(string)

        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), 0)
        self.assertEqual(len(matches), 1)

    def test_EndT(self):
        string = "Test Case"
        match = BaseTokens.EndT.value.search(string)
        matches = BaseTokens.EndT.value.findall(string)

        self.assertEqual(match.start(), len(string))
        self.assertEqual(match.end(), len(string))
        self.assertEqual(len(matches), 1)

    def test_ProperCaseWSpaces(self):
        string = "Test case"
        match = BaseTokens.ProperCaseWSpaces.value.search(string)

        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), 4)

        string = "Test Case"
        match = BaseTokens.ProperCaseWSpaces.value.search(string)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(string))

    def test_CapsWSpaces(self):
        string = "Test Case"
        match = BaseTokens.CapsWSpaces.value.search(string)

        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), 1)

        string = "TEST CASE"
        match = BaseTokens.CapsWSpaces.value.search(string)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(string))

    def test_LowerCaseWSpaces(self):
        string = "test Case"
        match = BaseTokens.LowerCaseWSpaces.value.search(string)

        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), 4)

        string = "test case"
        match = BaseTokens.LowerCaseWSpaces.value.search(string)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(string))

    def test_AlphabetsWSpaces(self):
        string = "Test Case"
        match = BaseTokens.AlphabetsWSpaces.value.search(string)

        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(string))

        string = "test case"
        match = BaseTokens.AlphabetsWSpaces.value.search(string)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(string))
