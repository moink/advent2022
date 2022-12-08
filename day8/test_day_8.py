import unittest

import numpy as np

from day8.day8 import get_treeline_visibility


class TestVisibility(unittest.TestCase):
    def test_get_treeline_visibility(self):
        test_cases = [
            ([5, 3, 5, 3], 2),
            ([5, 3], 1),
            ([5, 1, 2], 2),
            ([5, 5, 2], 1),
        ]
        for tree_line, expected_result in test_cases:
            test_vec = np.asarray(tree_line)
            result = get_treeline_visibility(test_vec)
            self.assertEqual(expected_result, result)

if __name__ == '__main__':
    unittest.main()
