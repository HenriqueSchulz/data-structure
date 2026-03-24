from data import Data


class Node:
    '''Node class for Search Tree'''

    def __init__(self, value: Data):
        self.data: Data = value
        self.left: None | SearchTree = None
        self.right: None | SearchTree = None
        self.height = 1


class SearchTree:
    '''Implements a binary search tree data structure.'''

    def __init__(self, balance, value=None):
        self.root: Node | None = Node(value) if value is not None else None
        self.balance = balance

    def insert(self, value: Data, iterations=0):
        '''
        Dispatcher for insert method.
        Uses recursive version if balanced, iterative otherwise.
        '''
        if self.balance:
            return self.insert_recursive(value, iterations)
        else:
            return self.insert_iterative(value, iterations)

    def insert_recursive(self, value: Data, iterations=0):
        '''Recursive insert (used for balanced tree).'''

        iterations += 1

        if self.root is None:
            self.root = Node(value)
            return iterations

        if value.salary == self.root.data.salary:
            return iterations

        # Insert left
        if value.salary < self.root.data.salary:
            if self.root.left is None:
                self.root.left = SearchTree(value=value, balance=self.balance)
            else:
                iterations += self.root.left.insert_recursive(value)

        # Insert right
        else:
            if self.root.right is None:
                self.root.right = SearchTree(value=value, balance=self.balance)
            else:
                iterations += self.root.right.insert_recursive(value)

        # Balance on unwind
        self._update_height()
        self._balance()

        return iterations

    def insert_iterative(self, value: Data, iterations=0):
        '''Iterative insert (used for unbalanced tree to avoid recursion overflow).'''

        iterations += 1

        if self.root is None:
            self.root = Node(value)
            return iterations

        current = self

        while True:
            iterations += 1

            if value.salary == current.root.data.salary:
                return iterations

            # Go left
            if value.salary < current.root.data.salary:
                if current.root.left is None:
                    current.root.left = SearchTree(value=value, balance=self.balance)
                    return iterations
                current = current.root.left

            # Go right
            else:
                if current.root.right is None:
                    current.root.right = SearchTree(value=value, balance=self.balance)
                    return iterations
                current = current.root.right

    def get(self, key):
        '''Searches for a value by key (salary).'''

        iterations = 0
        current = self

        while current is not None and current.root is not None:

            iterations += 1

            if key == current.root.data.salary:
                return current.root.data, iterations

            elif key < current.root.data.salary:
                current = current.root.left
            else:
                current = current.root.right

        return None, iterations


    def _get_height(self, subtree):
        if subtree is None or subtree.root is None:
            return 0
        return subtree.root.height

    def _get_balance_factor(self):
        return self._get_height(self.root.left) - self._get_height(self.root.right)

    def _update_height(self):
        left_height = self._get_height(self.root.left)
        right_height = self._get_height(self.root.right)
        self.root.height = 1 + max(left_height, right_height)

    def _balance(self):
        balance = self._get_balance_factor()

        # LEFT HEAVY
        if balance > 1:
            if self.root.left._get_balance_factor() < 0:
                self.root.left._rotate_left()
            self._rotate_right()

        # RIGHT HEAVY
        elif balance < -1:
            if self.root.right._get_balance_factor() > 0:
                self.root.right._rotate_right()
            self._rotate_left()

    def _rotate_left(self):
        right_tree = self.root.right
        new_root = right_tree.root

        T2 = new_root.left

        new_left_tree = SearchTree(balance=self.balance)
        new_left_tree.root = self.root

        new_left_tree.root.right = T2
        new_root.left = new_left_tree

        self.root = new_root

        self.root.left._update_height()
        self._update_height()

    def _rotate_right(self):
        left_tree = self.root.left
        new_root = left_tree.root

        T3 = new_root.right

        new_right_tree = SearchTree(balance=self.balance)
        new_right_tree.root = self.root

        new_right_tree.root.left = T3
        new_root.right = new_right_tree

        self.root = new_root

        self.root.right._update_height()
        self._update_height()