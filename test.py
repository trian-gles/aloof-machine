import unittest
import live_unit

class TestFilter(unittest.TestCase):
    def setUp(self):
        self.filter = live_unit.LiveFilter(3)
    
    def test_filter(self):
        output = self.filter.input(1)

        self.assertEqual(output, 1)

        output = self.filter.input(3)

        self.assertEqual(output, 2)

        output = self.filter.input(7)
        self.assertEqual(output, 11 / 3)

        output = self.filter.input(2)
        self.assertEqual(output, 4)

unittest.main()