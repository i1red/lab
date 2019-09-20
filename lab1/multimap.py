from collections import deque

class MultiMap:
    """Mapping class based on AVL Tree.

    Data is stored as a key and linked list of objects.
    """
    def __init__(self):
        self._root = None
        self._length = 0

    def __len__(self):
        return self._length

    def __setitem__(self, key, value):
        self._root = self._insert(self._root, key, value)

    def __iter__(self):
        return MultiMap._traversal(self._root)

    class Node:
        def __init__(self, key, obj):
            self.key = key
            self.items = deque([obj])
            self.height = 1
            self.lt = self.rt = None

        @property
        def bal_factor(self):
            return MultiMap._get_height(self.rt) - MultiMap._get_height(self.lt)

        def update_height(self):
            self.height = 1 + max(MultiMap._get_height(self.lt), MultiMap._get_height(self.rt))

    @staticmethod
    def _get_height(tree_node: Node) -> int:
        return 0 if tree_node is None else tree_node.height

    def _insert(self, cur, key, obj) -> Node:
        if cur is None:
            self._length += 1
            return MultiMap.Node(key, obj)

        if cur.key == key:
            self._length += 1
            cur.items.append(obj)
            return cur
        elif cur.key > key:
            cur.lt = self._insert(cur.lt, key, obj)
        else:
            cur.rt = self._insert(cur.rt, key, obj)

        return MultiMap._balance(cur)

    def _remove(self, cur, key) -> 'Node, None':
        if cur is None:
            return None

        if cur.key == key:
            self._length -= len(cur.items)
            if cur.rt is None:
                return cur.lt
            min_node = MultiMap._find_min(cur.rt)
            cur.key, cur.items = min_node.key, min_node.items
            cur.rt = self._remove(cur.rt, min_node.key)
        if cur.key > key:
            cur.lt = self._remove(cur.lt, key)
        else:
            cur.rt = self._remove(cur.rt, key)

        return MultiMap._balance(cur)

    @staticmethod
    def _balance(tree_node: Node) -> Node:
        tree_node.update_height()
        balance_factor = tree_node.bal_factor

        if balance_factor > 1:
            if tree_node.rt.bal_factor < 0:
                tree_node.rt = MultiMap._rotate_right(tree_node.rt)
            return MultiMap._rotate_left(tree_node)

        if balance_factor < -1:
            if tree_node.lt.bal_factor > 0:
                tree_node.lt = MultiMap._rotate_left(tree_node.lt)
            return MultiMap._rotate_right(tree_node)

        return tree_node

    @staticmethod
    def _rotate_left(tree_node: Node) -> Node:
        new_root, new_right = tree_node.rt, tree_node.rt.lt
        new_root.lt, tree_node.rt = tree_node, new_right

        tree_node.update_height()
        new_root.update_height()

        return new_root

    @staticmethod
    def _rotate_right(tree_node: Node) -> Node:
        new_root, new_left = tree_node.lt, tree_node.lt.rt
        new_root.rt, tree_node.lt = tree_node, new_left

        tree_node.update_height()
        new_root.update_height()

        return new_root

    @staticmethod
    def _traversal(cur: Node):
        if cur is not None:
            yield from MultiMap._traversal(cur.lt)
            for i in cur.items:
                yield (cur.key, i)
            yield from MultiMap._traversal(cur.rt)

    @staticmethod
    def _find_min(tree_node: Node) -> Node:
        while tree_node is not None and tree_node.lt is not None:
            tree_node = tree_node.lt

        return tree_node


    def popleft(self):
        obj = []
        self._remove_min(self._root, obj)
        return obj.pop()


    def _remove_min(self, tree_node: Node, container: list) -> Node:
        if tree_node.lt is None:
            container.append((tree_node.key, tree_node.items.popleft()))
            self._length -= 1
            return tree_node.rt if len(tree_node.items) == 0 else tree_node

        tree_node.lt = self._remove_min(tree_node.lt, container)
        return MultiMap._balance(tree_node)





a = MultiMap()
b = [1313, -223, 2323, -22, 0, 232, 3434]
import random
for i in range(10):
    random.shuffle(b)
    for i in b:
        a[i] = str(i)
    random.shuffle(b)

while len(a):
    print(a.popleft())