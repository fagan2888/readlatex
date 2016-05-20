import unittest

class TestLib(unittest.TestCase):
    def assertAlmostEqual(self, a, b, places=7):
        if isinstance(a, float):
            super().assertAlmostEqual(a, b, places=places)
            return
        if isinstance(a, list):
            super().assertEqual(len(a), len(b))
            for x, y in zip (a, b):
                super().assertAlmostEqual(x, y, places=places)
            return
        raise AssertionError("Incorrect argument types to assertAlmostEqual: " + str(a) + "; " + str(b))
