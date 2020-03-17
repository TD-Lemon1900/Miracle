import unittest
import random_r
from math import *

class TestMathFunc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(2, 1+1)

    def test_minus(self):
        self.assertEqual(1, 2 - 1)

    def test_multi(self):
        self.assertEqual(4, 2*2)

    def test_divide(self):
        self.assertEqual(3, 6/2)

    def test_dis(self):
        self.assertEqual(random_r.dis(1, 2, 1, 2), ((1 - 2)**2+(1 - 2)**2)**0.5)

if __name__ == "__main__":
    unittest.main(verbosity=2)