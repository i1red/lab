import unittest
from priorityqueue import *
from sortedkeycollections import SortedKeyList


class TestPriorityQueue(unittest.TestCase):
    def test_repr(self):
        qu_list = PriorityQueue(container=SortedKeyList)
        self.assertEqual(repr(qu_list), 'PriorityQueue([], SortedKeyList)')

        qu_avl = PriorityQueue()

        for i in range(6):
            qu_avl.put((i, i))
        self.assertEqual(repr(qu_avl), 'PriorityQueue([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], '
                                       'AVLTree)')

        qu_avl.put((6, 6))
        self.assertEqual(repr(qu_avl), 'PriorityQueue([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), ...], '
                                       'AVLTree)')

    def test_get_exception_expected(self):
        qu = PriorityQueue()
        self.assertRaises(queue.Empty, lambda: qu.get())

if __name__ == '__main__':
    unittest.main()
