
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
        a = Reference(Params.default, "def", 2, 34)
        b = Reference(Params.default, "def", 3, 34)
        c = Reference(Params.default, "e3d", 2, 34)
        self.assertTrue(a < b)
        self.assertEqual(a, c)

    def test_distance(self):
        a = Reference(Params.default, "abc", 2, 100)
        b = Reference(Params.default, "abc", 3, -20)
        self.assertEqual(120, a.distance(b))
        self.assertEqual(120, b.distance(a))

    def test_removability(self):
        p = Params(2.74, 0.334)
        abc = Figure("abc", 234)
        def2 = Figure("def", 642)
        a = Reference(p, "abc", 2, 100)
        b = Reference(p, "def", 3, 150)
        c = Reference(p, "abc", 4, 200)
        refs = [a,b,c]
        figs = Figures({"abc" : abc, "def" : def2})
        self.assertEqual(234 * (1/0.334 + 1/(50 + 1) + 2.74/(100 + 1)), a.removability(figs, refs))
        self.assertEqual(642 * (1/0.334 + 1/(50 + 1) + 1/(50 + 1)), b.removability(figs, refs))
        self.assertEqual(234 * (1/0.334 + 2.74/(100 + 1) + 1/(50 + 1)), c.removability(figs, refs))


class TestPages(unittest.TestCase):

    def test_locs_one_page(self):
        actual = get_pages(Params.default, "test/docs/locs_one_page", 1000)
        expected = { 1 : TestPages.get_page_1() }
        self.assertEqual(expected, actual)

    def test_locs_two_page(self):
        self.maxDiff = None
        actual = get_pages(Params.default, "test/docs/locs_two_page", 1000)
        expected = { 1 : TestPages.get_page_1(), 3 : TestPages.get_page_3() }
        self.assertEqual(expected, actual)

    def get_page_1():
        page1 = Page(Params.default, 1, 1000)
        page1._Page__refs = [
            Reference(Params.default, "b", 1, 20.0),
            Reference(Params.default, "a", 3, 20.0),
            Reference(Params.default, "c", 2, 30.0),
            Reference(Params.default, "a", 0, 100.0)
        ]
        return page1

    def get_page_3():
        page3 = Page(Params.default, 3, 1000)
        page3._Page__refs = [
            Reference(Params.default, "a", 6, 20.0),
            Reference(Params.default, "b", 4, 30.0),
            Reference(Params.default, "a", 5, 30.0)
        ]
        return page3

if __name__ == '__main__':
    unittest.main()
