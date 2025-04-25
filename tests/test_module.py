import unittest
from mypackage.module import add_int
from parameterized import parameterized

class TestModuleMethods(unittest.TestCase):

    def test_errors(self):

        with self.assertRaises(TypeError, msg="Expected integer argument for y."):
            add_int(1, "3")
        
        with self.assertRaises(TypeError, msg="Expected integer argument for x."):
            add_int({1,2}, 5)

    
    @parameterized.expand([
        [1, 2, 3],
        [-4, 10, 6],
        [1000, 100, 1100]
    ])
    def test_result(self, x, y, expected):

        self.assertEqual(add_int(x, y), expected)


if __name__ == "__main__":
    unittest.main()