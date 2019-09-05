import unittest
from priorityqueue import PriorityQueueList, PriorityQueueBST

class TestPriorityQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.test_class = PriorityQueueList

    def test_append(self):
        values_integer = [(21, '113'), (71, 'wcwf'), (-6, (121, 32, 'x')), (11, 232), (-6, 'seq'), (21, -50),
                          (-600000, 'adf'), (11, 'wwe')]
        prioritized_values_integer = [(-600000, 'adf'), (-6, (121, 32, 'x')), (-6, 'seq'), (11, 232), (11, 'wwe'),
                                      (21, '113'), (21, -50), (71, 'wcwf')]

        qu_integer = self.test_class()
        for priority, obj in values_integer:
            qu_integer.append(priority, obj)

        self.assertEqual(list(iter(qu_integer)), prioritized_values_integer)
        self.assertEqual(len(qu_integer), len(values_integer))

        values_str = [('xYz', '93242sax'), ('xYz', ('x', 823)), ('a97', -23), ('a', 'xx'), ('HH', -23.6), ('a', 132),
                      ('77', 32)]
        prioritized_values_str = [('77', 32), ('HH', -23.6), ('a', 'xx'), ('a', 132), ('a97', -23), ('xYz', '93242sax'),
                                  ('xYz', ('x', 823))]

        qu_str = self.test_class()
        for priority, obj in values_str:
            qu_str.append(priority, obj)

        self.assertEqual(list(iter(qu_str)), prioritized_values_str)
        self.assertEqual(len(qu_str), len(values_str))


    def test_pop(self):
        qu = self.test_class([((12, 'x'), 78.5), ((-10, 'X'), 'wca'), ((12, '8'), '87'), ((-10, 'X'), 212121)])
        values = [((12, 'x'), 78.5), ((12, '8'), '87'), ((-10, 'X'), 212121), ((-10, 'X'), 'wca')]

        while qu:
            self.assertEqual(qu.pop(), values.pop())

        self.assertEqual(len(qu), 0)


    def test_repr(self):
        qu = self.test_class()
        tested_class = type(qu).__name__
        self.assertEqual(repr(qu), f'{tested_class}()')

        for i in range(6):
            qu.append(i, i)
        self.assertEqual(repr(qu), f'{tested_class}([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])')

        qu.append(6, 6)
        self.assertEqual(repr(qu), f'{tested_class}([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), ...])')


class TestPriorityQueueBST(TestPriorityQueue):
    def setUp(self) -> None:
        self.test_class = PriorityQueueBST


if __name__ == '__main__':
    unittest.main()