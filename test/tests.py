
import sys
import os

sys.path.append("src")

from end_to_end_test import *
from testlib import *

from readlatex_calc import *
import unittest
from readlatex_params import *
from readlatex_engine import *

class TestReference(TestLib):
    def test_basic_compare(self):
        a = Reference(Params.default, "abc", 2, 34)
        b = Reference(Params.default, "abc", 2, 24)
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
        p = Params(penalty_height=0.334, penalty_duplication=1.74)
        abc = Figure("abc", 234)
        def2 = Figure("def", 642)
        a = Reference(p, "abc", 2, 100)
        b = Reference(p, "def", 3, 150)
        c = Reference(p, "abc", 4, 200)
        refs = [a,b,c]
        figs = Figures({"abc" : abc, "def" : def2})
        self.assertEqual(234 * (0.334 + 1/(50 + 1) + 2.74/(100 + 1)), a.removability(figs, refs))
        self.assertEqual(642 * (0.334 + 1/(50 + 1) + 1/(50 + 1)), b.removability(figs, refs))
        self.assertEqual(234 * (0.334 + 2.74/(100 + 1) + 1/(50 + 1)), c.removability(figs, refs))

    figs = Figures({"a" : Figure("a", 20), "b" : Figure("b", 60), "c": Figure("c", 40)})

    def test_does_not_remove_when_lots_of_space(self):
        page1 = TestPages.get_page_1(Params.default)
        page1._Page__height = float('inf')
        page1c = TestPages.get_page_1(Params.default)
        page1.remove_extras(TestReference.figs)
        self.assertEqual(page1c._Page__refs, page1._Page__refs)

    def test_0_removes_everything(self):
        page1 = TestPages.get_page_1(Params.default)
        page1._Page__height = 0
        page1c = TestPages.get_page_1(Params.default)
        page1.remove_extras(TestReference.figs)
        self.assertEqual([], page1._Page__refs)


class TestRemove(TestLib):
    def test_remove_by_height(self):
        """
        Layout of page

        20:     b[60] a[20]
        30:     c[40]

        100:    a[20]

        So the biggest
        """
        p = Params(penalty_height=100000, penalty_duplication=1) # all that matters is height
        page1 = TestPages.get_page_1(p)
        page1._Page__height = 100
        page1c = TestPages.get_page_1(p)
        page1.remove_extras(TestReference.figs)
        page1c._Page__refs.pop(0) # delete the largest item, the "b" reference
        self.assertEqual(page1c._Page__refs, page1._Page__refs)

    def test_remove_duplicates(self):
        # see above for layout of page
        p = Params(penalty_height=1, penalty_duplication=100000) # all that matters is duplication
        page1 = TestPages.get_page_1(p)
        page1._Page__height = 120
        page1c = TestPages.get_page_1(p)
        page1.remove_extras(TestReference.figs)
        page1c._Page__refs.pop(1) # delete the largest item, the "b" reference
        self.assertEqual(len(page1c._Page__refs), len(page1._Page__refs))
        self.assertEqual(page1c._Page__refs, page1._Page__refs)

    def test_initial_layout(self):
        # see above for layout of page
        p = Params(penalty_duplication=1000, # get rid of dups
                    resolution_iterations = 0 # don't actually run resolver
                    )
        page1 = TestPages.get_page_1(p)
        page1._Page__height = 128
        """
        Layout afterwards
        20:     b[60]
        30:     c[40]

        100:    a[20]
        """
        page1.remove_extras(TestReference.figs)
        ys = page1._Page__resolver(TestReference.figs).ys
        self.assertEqual([32, 84, 116], ys)

    def test_no_conflict(self):
        p = Params()
        page = TestPages.get_no_conflict_page()
        before = list(page._Page__refs)
        page.resolve(TestReference.figs)
        after = list(page._Page__refs)
        self.assertEqual(before, after)

    def test_resolver(self):
        # see above for layout of page
        p = Params(penalty_duplication=1000, # get rid of dups
                    resolution_iterations = 1000 # lots of iterations!
                    )
        page1 = TestPages.get_page_1(p)
        page1._Page__height = 128
        """
        Layout afterwards
        20:     b[60]
        30:     c[40]

        100:    a[20]

        So they should all be stacked at the bottom under ideal circumstances.
        """
        page1.resolve(TestReference.figs)
        self.assertAlmostEqual([30, 80, 110], [ref.position for ref in page1._Page__refs], places=3)


class TestPages(TestLib):

    def test_locs_one_page(self):
        actual = get_pages(Params.default, "test/docs/locs_one_page", 1000)
        expected = { 1 : TestPages.get_page_1(Params.default) }
        self.assertEqual(expected, actual)

    def test_locs_two_page(self):
        self.maxDiff = None
        actual = get_pages(Params.default, "test/docs/locs_two_page", 1000)
        expected = { 1 : TestPages.get_page_1(Params.default), 3 : TestPages.get_page_3() }
        self.assertEqual(expected, actual)

    def get_page_1(p):
        page1 = Page(p, 1, 1000)
        page1._Page__refs = [
            Reference(p, "b", 1, 20.0),
            Reference(p, "a", 3, 20.0),
            Reference(p, "c", 2, 30.0),
            Reference(p, "a", 0, 100.0)
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

    def get_no_conflict_page():
        page = Page(Params(), 1, 1000)
        page._Page__refs = [
            ## 0 -- a -- 20 -- b -- 80 -- gap -- 400 -- c -- 440
            Reference(Params(), "a", 3, 10),
            Reference(Params(), "b", 2, 50),
            Reference(Params(), "c", 1, 420)
        ]
        return page

if __name__ == '__main__':
    unittest.main()
