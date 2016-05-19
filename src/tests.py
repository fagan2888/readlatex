
from readlatex_calc import *
import unittest

class TestReference(unittest.TestCase):
    def test_basic_compare(self):
        a = Reference("abc", 2, 34)
        b = Reference("abc", 2, 24)
        self.assertTrue(b < a)
        self.assertTrue(a > b)
        self.assertTrue(a != b)
        self.assertTrue(b != a)
        self.assertTrue(a == a)
        self.assertTrue(b == b)
    def test_complex_compare(self):
        a = Reference("def", 2, 34)
        b = Reference("def", 3, 34)
        c = Reference("e3d", 2, 34)
        self.assertTrue(a < b)
        self.assertEqual(a, c)


if __name__ == '__main__':
    unittest.main()
