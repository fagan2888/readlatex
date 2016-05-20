import unittest
import subprocess
from os import remove

from testlib import *

PYTHON="python3"

class SmokeTest(TestLib):
    def test_basic_smoke(self):
        self.assertEqual(0, shellreadlatex("test/docs/smoke_test.tex"))


def shellreadlatex(path):
    with open("__log__", "w") as f:
        value = subprocess.call([PYTHON, "src/readlatex.py", path], stdout=f, stderr=f)
        if value == 0:
            remove("__log__")
        return value