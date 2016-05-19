
import sys
import os

sys.path.append("src")

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

class TestPages(unittest.TestCase):

    def test_locs_one_page(self):
        actual = get_pages("test/docs/locs_one_page")
        expected = { 1 : TestPages.get_page_1() }
        self.assertEqual(expected, actual)

    def test_locs_two_page(self):
        self.maxDiff = None
        actual = get_pages("test/docs/locs_two_page")
        expected = { 1 : TestPages.get_page_1(), 3 : TestPages.get_page_3() }
        self.assertEqual(expected, actual)

    def get_page_1():
        page1 = Page(1)
        page1._Page__refs = [
            Reference("b", 1, 2.0),
            Reference("a", 3, 2.0),
            Reference("c", 2, 3.0),
            Reference("a", 0, 134.0)
        ]
        return page1

    def get_page_3():
        page3 = Page(3)
        page3._Page__refs = [
            Reference("a", 6, 23.0),
            Reference("b", 4, 34.0),
            Reference("a", 5, 34.0)
        ]
        return page3

if __name__ == '__main__':
    unittest.main()
