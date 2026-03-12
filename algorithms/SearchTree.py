class Node:
    '''Node class for Search Tree'''

    def __init__(self, value):
        self.data = value
        self.left: None | SearchTree = None
        self.right: None | SearchTree = None
        self.height = 1

class SearchTree:
    '''Implements a binary search tree data structure.'''

    def __init__(self, value = None, balance: bool = True):    
            self.root: Node | None = Node(value) if value is not None else None
            self.balance = balance

    def insert(self, value):
        '''Inserts a value into the search tree. complexity: O(log n) on average, O(n) in worst case'''

        if self.root is None:
            self.root = Node(value)
            return
        
        #Insert left
        if value < self.root.data:
            if self.root.left is None:
                self.root.left = SearchTree(value)
            else:
                self.root.left.insert(value)
        
        #Insert right
        else:
            if self.root.right is None:
                self.root.right = SearchTree(value)
            else:
                self.root.right.insert(value)
        
        self._update_height()
        
        if self.balance:
            self._balance()

    def _get_height(self, subtree):
        '''Returns the height of the given subtree. complexity: O(1)'''

        if subtree is None or subtree.root is None:
            return 0
        return subtree.root.height
    
    def _get_balance_factor(self):
        '''Returns the balance factor of the current root. complexity: O(1) on average, O(log n) in worst case'''
        return self._get_height(self.root.left) - self._get_height(self.root.right)

    def _update_height(self):
        '''Updates the height of the current root. complexity: O(1)'''

        left_height = self._get_height(self.root.left)
        right_height = self._get_height(self.root.right)

        self.root.height = 1 + max(left_height, right_height)
    
    def _balance(self):
        '''Balances the search tree. complexity: O(1)'''

        balance = self._get_balance_factor()

        # LEFT HEAVY
        if balance > 1:

            # Left-Right case
            if self.root.left._get_balance_factor() < 0:
                self.root.left._rotate_left()

            # Left-Left case
            self._rotate_right()

        # RIGHT HEAVY
        elif balance < -1:

            # Right-Left case
            if self.root.right._get_balance_factor() > 0:
                self.root.right._rotate_right()

            # Right-Right case
            self._rotate_left()

    def _rotate_left(self):
        '''Performs a left rotation on the search tree. complexity: O(1)'''

        # The right subtree of the current root will become the new root
        right_tree = self.root.right
        new_root = right_tree.root

        # T2 is the left subtree of the new root
        T2 = new_root.left

        # Create a new SearchTree that will hold the old root (z)
        new_left_tree = SearchTree()
        new_left_tree.root = self.root

        # The T2 subtree becomes the right subtree of the old root
        new_left_tree.root.right = T2

        # Attach the old root as the left subtree of the new root
        new_root.left = new_left_tree

        # Update the tree root
        self.root = new_root

        #Update heights
        self.root.left._update_height()
        self._update_height()
    
    def _rotate_right(self):
        '''Performs a right rotation on the search tree. complexity: O(1)'''

        # The left subtree of the current root will become the new root
        left_tree = self.root.left
        new_root = left_tree.root

        # T3 is the right subtree of the new root (y)
        T3 = new_root.right

        # Create a new SearchTree that will hold the old root (z)
        new_right_tree = SearchTree()
        new_right_tree.root = self.root

        # The T3 subtree becomes the left subtree of the old root
        new_right_tree.root.left = T3

        # Attach the old root as the right subtree of the new root
        new_root.right = new_right_tree

        # Update the tree root
        self.root = new_root

        #Update heights
        self.root.right._update_height()
        self._update_height()