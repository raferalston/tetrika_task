import unittest
from solution import strict, sum_two

class TestStrictDecorator(unittest.TestCase):
    def test_sum_two_correct_types(self):
        """Test sum_two works with correct integer inputs"""
        self.assertEqual(sum_two(1, 2), 3)
        self.assertEqual(sum_two(-1, 1), 0)
        self.assertEqual(sum_two(0, 0), 0)

    def test_sum_two_first_arg_wrong_type(self):
        """Test TypeError raised when first argument is wrong type"""
        with self.assertRaises(TypeError):
            sum_two(1.5, 2)

    def test_sum_two_second_arg_wrong_type(self):
        """Test TypeError raised when second argument is wrong type"""
        with self.assertRaises(TypeError):
            sum_two(1, 2.5)

    def test_decorator_preserves_function(self):
        """Test that decorator preserves original function behavior"""
        def add(x: int, y: int) -> int:
            return x + y
            
        self.assertEqual(add(1, 2), sum_two(1, 2))

    def test_strict_with_different_function(self):
        """Test decorator works with a different function"""
        @strict
        def multiply(x: int, y: int) -> int:
            return x * y
            
        self.assertEqual(multiply(2, 3), 6)
        with self.assertRaises(TypeError):
            multiply(2.0, 3)

if __name__ == '__main__':
    unittest.main()