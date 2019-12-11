import collections


class AVLTree:
    class Node:
        def __init__(self, key, value, left=None, right=None):
            self.key = key
            self.values = collections.deque([value])
            self.left = left
            self.right = right
            self.height = 1
            self._parent = None

        @property
        def left(self):
            return self._left

        @left.setter
        def left(self, child):
            self._left = child
            if child is not None:
                child._parent = self

        @property
        def right(self):
            return self._right

        @right.setter
        def right(self, child):
            self._right = child
            if child is not None:
                child._parent = self

        @property
        def parent(self):
            return self._parent

        def balance_factor(self):
            return (0 if self.right is None else self.right.height) - (0 if self.left is None else self.left.height)

        def update_height(self):
            self.height = max(0 if self.right is None else self.right.height,
                              0 if self.left is None else self.left.height) + 1

        def clear_parent(self):
            if self._parent is not None:
                if self is self._parent._left:
                    self._parent._left = None
                else:
                    self._parent._right = None
                self._parent = None

        #those methods are used only for testing balance
        def left_tree_height(self):
            return 0 if self.left is None else (max(self.left.left_tree_height(), self.left.right_tree_height()) + 1)

        def right_tree_height(self):
            return 0 if self.right is None else (max(self.right.left_tree_height(), self.right.right_tree_height()) + 1)

    def __init__(self):
        self._root = None
        self._length = 0

    def __len__(self):
        return self._length

    def __iter__(self):
        for node in self.node_iter():
            for value in node.values:
                yield (node.key, value)

    #this method allows to test balance using Node.left_tree_height, Node.right_tree_height
    #without ability to change tree structure
    def node_iter(self):
        node_stack = collections.deque()
        tmp = self._root
        while tmp is not None or len(node_stack) > 0:
            if tmp is not None:
                node_stack.append(tmp)
                tmp = tmp.left
            else:
                cur = node_stack.pop()
                yield cur
                tmp = cur.right

    def _reset_parent(self, prev_son, new_son, parent):
        if parent is None:
            self._root = new_son
            new_son.clear_parent()
        else:
            if prev_son is parent.left:
                parent.left = new_son
            else:
                parent.right = new_son

    def _rotate_right(self, node):
        node_parent, new_root, new_left = node.parent, node.left, node.left.right
        self._reset_parent(node, new_root, node_parent)
        node.left, new_root.right = new_left, node

        node.update_height()
        new_root.update_height()

    def _rotate_left(self, node):
        node_parent, new_root, new_right = node.parent, node.right, node.right.left
        self._reset_parent(node, new_root, node_parent)
        node.right, new_root.left = new_right, node

        node.update_height()
        new_root.update_height()

    def _fix_balance(self, node):
        bf = node.balance_factor()
        node_parent = node.parent

        if bf == -2:
            if node.left.balance_factor() > 0:
                self._rotate_left(node.left)
            self._rotate_right(node)
        elif bf == 2:
            if node.right.balance_factor() < 0:
                self._rotate_right(node.right)
            self._rotate_left(node)

        if node_parent is not None:
            node_parent.update_height()
            self._fix_balance(node_parent)

    def insert(self, key, value):
        if self._root is None:
            self._root = AVLTree.Node(key, value)
        else:
            tmp = self._root
            while True:
                if key > tmp.key:
                    if tmp.right is None:
                        tmp.right = AVLTree.Node(key, value)
                        tmp.update_height()
                        self._fix_balance(tmp)
                        break
                    else:
                        tmp = tmp.right
                elif key == tmp.key:
                    tmp.values.append(value)
                    break
                else:
                    if tmp.left is None:
                        tmp.left = AVLTree.Node(key, value)
                        tmp.update_height()
                        self._fix_balance(tmp)
                        break
                    else:
                        tmp = tmp.left

        self._length += 1

    def popleft(self):
        if self._root is None:
            raise KeyError('Pop from empty tree')
        if self._root.left is None:
            key_value = (self._root.key, self._root.values.popleft())
            if len(self._root.values) == 0:
                self._root = self._root.right
        else:
            tmp = self._root
            while tmp.left.left is not None:
                tmp = tmp.left

            key_value = (tmp.left.key, tmp.left.values.popleft())
            if len(tmp.left.values) == 0:
                tmp.left = tmp.left.right
                tmp.update_height()
                self._fix_balance(tmp)

        self._length -= 1
        return key_value


class SortedKeyList:
    class Node:
        def __init__(self, key, value, next=None):
            self.key = key
            self.value = value
            self.next = next

    def __init__(self):
        self._head = None
        self._length = 0

    def __len__(self):
        return self._length

    def __iter__(self):
        tmp = self._head
        while tmp is not None:
            yield (tmp.key, tmp.value)
            tmp = tmp.next

    def insert(self, key, value):
        if self._head is None:
            self._head = SortedKeyList.Node(key, value)
        elif self._head.key > key:
            self._head = SortedKeyList.Node(key, value, self._head)
        else:
            tmp = self._head
            while tmp.next is not None and tmp.next.key <= key:
                tmp = tmp.next
            tmp.next = SortedKeyList.Node(key, value, tmp.next)

        self._length += 1

    def popleft(self):
        if self._head is None:
            raise KeyError('Pop from empty list')

        key_value = (self._head.key, self._head.value)
        self._head = self._head.next
        self._length -= 1
        return key_value


class SortedArrayList:
    def __init__(self):
        self._container = []

    def __len__(self):
        return len(self._container)

    def __iter__(self):
        return iter(self._container)

    def insert(self, key, value):
        self._container.append((key, value))

        i = len(self) - 1
        while i > 0 and self._container[i][0] < self._container[i - 1][0]:
            self._container[i], self._container[i - 1] = self._container[i - 1], self._container[i]
            i -= 1

    def popleft(self):
        if len(self) == 0:
            raise KeyError('Pop from empty list')

        return self._container.pop(0)




