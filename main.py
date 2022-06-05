import unittest


def additon(*args):
    result = 0
    for arg in args:
        result += arg
    return result


class AdditionTestCase(unittest.TestCase):
    def test_addition_two_params(self):
        result = additon(3, 2)
        assert result == 5

    def test_addition_three_params(self):
        result = additon(3, 2, 1)
        assert result == 6

    def test_addition_zero_params(self):
        result = additon()
        assert result == 0


if __name__ == '__main__':
    unittest.main(verbosity=2)
