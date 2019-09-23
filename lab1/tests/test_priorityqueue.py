import unittest
from lab1.priorityqueue import *
from lab1.sortedkeycollections import SortedKeyList


class TestPriorityQueue(unittest.TestCase):
    def test_repr(self):
        qu_list = PriorityQueue(container=SortedKeyList)
        self.assertEqual(repr(qu_list), 'PriorityQueue([], lab1.sortedkeycollections.SortedKeyList)')

        qu_avl = PriorityQueue()

        for i in range(6):
            qu_avl.put((i, i))
        self.assertEqual(repr(qu_avl), 'PriorityQueue([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], '
                                       'lab1.sortedkeycollections.AVLTree)')

        qu_avl.put((6, 6))
        self.assertEqual(repr(qu_avl), 'PriorityQueue([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), ...], '
                                       'lab1.sortedkeycollections.AVLTree)')

    def test_get_exception_expected(self):
        qu = PriorityQueue()
        self.assertRaises(queue.Empty, lambda: qu.get())

if __name__ == '__main__':
    unittest.main()
