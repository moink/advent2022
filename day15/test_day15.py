import unittest

from day15 import split_zone

class MyTestCase(unittest.TestCase):
    def test_one(self):
        zone = (0, 40, 0, 40)
        result ={i for i in split_zone(zone)}
        expected_result = {
            (0, 20, 0, 20),
            (21, 40, 0, 20),
            (0, 20, 21, 40),
            (21, 40, 21, 40)
        }
        self.assertEqual(expected_result, result)

    def test_two(self):
        zone = (0, 1, 0, 1)
        result ={i for i in split_zone(zone)}
        expected_result = {
            (0, 0, 0, 0),
            (0, 0, 1, 1),
            (1, 1, 0, 00),
            (1, 1, 1, 1)
        }
        self.assertEqual(expected_result, result)

    def test_three(self):
        zone = (7, 20, 1, 1)
        result = {i for i in split_zone(zone)}
        expected_result = {
            (7, 13, 1, 1),
            (14, 20, 1, 1),
        }
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
