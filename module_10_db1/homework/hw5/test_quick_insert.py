import unittest
from quick_insert import find_insert_position


class TestQuickInsert(unittest.TestCase):
    """ Test function find_insert_position() """

    def setUp(self):
        self.list_more_one_element = [1, 2, 3, 3, 3, 5]
        self.list_one_element = [3]
        self.list_empty = []
        self.x = 4

    def test_more_one_element(self):
        result = find_insert_position(self.list_more_one_element, self.x)
        self.assertEqual(result, 5)

    def test_one_element_x_more(self):
        result = find_insert_position(self.list_one_element, self.x)
        self.assertEqual(result, 1)

    def test_empty(self):
        result = find_insert_position(self.list_empty, self.x)
        self.assertEqual(result, 0)

    def test_one_element_x_less(self):
        x = 2
        result = find_insert_position(self.list_more_one_element, x)
        self.assertEqual(result, 1)

    def test_sorting_list(self):
        position = find_insert_position(self.list_more_one_element, self.x)
        self.list_more_one_element.insert(position, self.x)
        self.assertEqual(self.list_more_one_element, sorted(self.list_more_one_element))


if __name__ == '__main__':
    unittest.main()
