import unittest
import random
from lab1.sortedkeycollections import AVLTree, SortedKeyList


class TestSortedKeyList(unittest.TestCase):
    def setUp(self):
        self.test_class = SortedKeyList

    def test_insert(self):
        values_integer = [(21, '113'), (71, 'wcwf'), (-6, (121, 32, 'x')), (11, 232), (-6, 'seq'), (21, -50),
                          (-600000, 'adf'), (11, 'wwe')]
        prioritized_values_integer = [(-600000, 'adf'), (-6, (121, 32, 'x')), (-6, 'seq'), (11, 232), (11, 'wwe'),
                                      (21, '113'), (21, -50), (71, 'wcwf')]

        collection_integer = self.test_class()
        for pair in values_integer:
            collection_integer.insert(*pair)

        self.assertEqual(list(iter(collection_integer)), prioritized_values_integer)
        self.assertEqual(len(collection_integer), len(values_integer))

        values_str = [('xYz', '93242sax'), ('xYz', ('x', 823)), ('a97', -23), ('a', 'xx'), ('HH', -23.6), ('a', 132),
                      ('77', 32)]
        prioritized_values_str = [('77', 32), ('HH', -23.6), ('a', 'xx'), ('a', 132), ('a97', -23), ('xYz', '93242sax'),
                                  ('xYz', ('x', 823))]

        collection_str = self.test_class()
        for priority, obj in values_str:
            collection_str.insert(priority, obj)

        self.assertEqual(list(iter(collection_str)), prioritized_values_str)
        self.assertEqual(len(collection_str), len(values_str))

    def test_popleft(self):
        if self.test_class is None:
            return

        values = [((12, 'x'), 78.5), ((-10, 'X'), 'wca'), ((12, '8'), '87'), ((-10, 'X'), 212121)]
        expected_values = [((12, 'x'), 78.5), ((12, '8'), '87'), ((-10, 'X'), 212121), ((-10, 'X'), 'wca')]
        collection = self.test_class()
        for pair in values:
            collection.insert(*pair)

        while len(collection) > 0:
            self.assertEqual(collection.popleft(), expected_values.pop())

    def test_popleft_exception(self):
        collection = self.test_class()
        self.assertRaises(KeyError, lambda: collection.popleft())

class TestAVLTree(TestSortedKeyList):
    def setUp(self):
        self.test_class = AVLTree



if __name__ == '__main__':
    unittest.main()
