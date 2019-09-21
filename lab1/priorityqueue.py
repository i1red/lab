import reprlib
import lab1.sortedkeycollections as kscollections
import queue


class PriorityQueue:
    def __init__(self, pairs=None, container=kscollections.AVLTree):
        self.container = container()
        if pairs is not None:
            for pair in pairs:
                self.put(pair)

    def __len__(self):
        return len(self.container)

    def __repr__(self):
        container_type, container_module = self.container.__class__.__name__, self.container.__class__.__module__
        container_name = ('' if container_module is None or container_module == str.__class__.__module__
                          else container_module + '.') + container_type
        return f'PriorityQueue({reprlib.repr(list(iter(self.container)))}, {container_name})'

    def put(self, pair):
        self.container.insert(*pair)

    def get(self):
        try:
            return self.container.popleft()
        except KeyError:
            raise queue.Empty('Can not get pair. Queue is empty')

