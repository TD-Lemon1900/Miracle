import unittest
import matplotlib.pyplot as plt
import numpy as np
# from uiiii import Board


class TestgBoard(unittest.TestCase):
    def test_update(self):
        N = 400
        s = np.ones((N, N))
        s2 = np.zeros((N, N))
        for i in range(1, N - 1):
            for j in range(1, N - 1):
                arround = np.array([[s[i - 1, j - 1], s[i - 1, j], s[i - 1, j + 1]],
                                    [s[i, j - 1], 0, s[i, j + 1]],
                                    [s[i + 1, j - 1], s[i + 1, j], s[i + 1, j + 1]]])
                if arround.sum() == 3:
                    s2[i, j] = 1
                elif s[i, j] == 0 and arround.sum() == 2:
                    s2[i, j] = 0
                elif s[i, j] == 1 and arround.sum() == 2:
                    s2[i, j] = 1
                else:
                    s2[i, j] = 0
        s3 = np.zeros((N, N))
        self.assertEqual(s2.all(), s3.all())


if __name__ == '__main__':
    unittest.main(verbosity=2)