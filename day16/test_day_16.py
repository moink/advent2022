import unittest

from day16 import ParetoSet


class TestParetoSet(unittest.TestCase):
    def test_add(self):
        s = ParetoSet()
        s.add(())


if __name__ == '__main__':
    unittest.main()
