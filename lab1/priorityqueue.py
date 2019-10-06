import reprlib
import lab1.sortedkeycollections as skcollections
import queue


class PriorityQueue:
    def __init__(self, pairs=None, container=skcollections.AVLTree):
        self.container = container()
        if pairs is not None:
            for pair in pairs:
                self.put(pair)

    def __bool__(self):
        return bool(len(self.container))

    def __repr__(self):
        container_type = self.container.__class__.__name__
        return f'PriorityQueue({reprlib.repr(list(iter(self.container)))}, {container_type})'

    def put(self, pair):
        self.container.insert(*pair)

    def get(self):
        try:
            return self.container.popleft()
        except KeyError:
            raise queue.Empty('Can not get pair. Queue is empty')

