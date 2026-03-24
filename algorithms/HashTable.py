from data import Data


class HashTable:
    '''Implements a hash table data structure using separate chaining for collision resolution.'''
    
    def __init__(self, size, hash_type='modular'):
        self.size = size
        self.table: list[list[Data]] = [[] for _ in range(size)]
        self.hash_type = hash_type
        self.ocupation = 0
        self.collisions = 0  # NEW: collision counter

        if hash_type not in ['modular', 'multiplicative', 'universal']:
            raise ValueError("Unsupported hash type. Use chose between modular, multiplicative, or universal.")
        
        self.A = 0.6180339887
        self.p = 109345121
        self.a = 31415
        self.b = 27183

    def _hash(self, key):
        
        if self.hash_type == "modular":
            return key % self.size

        elif self.hash_type == "multiplicative":
            return int(self.size * ((key * self.A) % 1))

        elif self.hash_type == "universal":
            return ((self.a * key + self.b) % self.p) % self.size
    
    def insert(self, value: Data, key=None):
        '''
        Inserts a key-value pair into the hash table.
        Average: O(1), Worst-case: O(n) due to collisions.
        Also tracks collisions.
        '''

        iterations = 1

        if key is None:
            key = value.salary

        index = self._hash(key)

        if len(self.table[index]) > 0:
            self.collisions += 1

        # Insert (separate chaining)
        self.table[index].append([key, value])

        # Track occupation
        if len(self.table[index]) == 1:
            self.ocupation += 1

        return iterations
    
    def get(self, key):
        '''Searches for a value by key (salary). complexity: O(1) average, O(n) worst case'''

        index = self._hash(key)

        iterations = 0

        for k, v in self.table[index]:

            iterations += 1

            if k == key:
                return v, iterations

        return None, iterations
    
    def load_factor(self):
        '''Calculates the load factor of the hash table.'''
        return self.ocupation / self.size

    def get_collisions(self):
        '''Returns total number of collisions occurred during insertions.'''
        return self.collisions

    def delete(self, key):
        '''Deletes the key-value pair associated with the given key.'''

        index = self._hash(key)

        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True

        return False

    def display(self):
        '''Displays the contents of the hash table.'''

        for i, bucket in enumerate(self.table):
            print(f"{i}: {bucket}")