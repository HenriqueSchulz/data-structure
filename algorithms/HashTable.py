from data import Data

class HashTable:
    '''Implements a hash table data structure using separate chaining for collision resolution.'''
    
    def __init__(self, size, hash_type='modular'):
        self.size = size
        self.table: list[list[Data]] = [[] for _ in range(size)]
        self.hash_type = hash_type
        self.ocupation = 0

        if hash_type not in ['modular', 'multiplicative', 'universal']:
            raise ValueError("Unsupported hash type. Use chose between modular, multiplicative, or universal.")
        
        self.A = 0.6180339887  # Knuth's constant for multiplicative hashing
        self.p = 109345121     # A large prime for universal hashing
        self.a = 31415         # Randomly chosen for universal hashing
        self.b = 27183         # Randomly chosen for universal hashing

    def _hash(self, key):
        
        if self.hash_type == "modular":
            return key % self.size

        elif self.hash_type == "multiplicative":
            return int(self.size * ((key * self.A) % 1))

        elif self.hash_type == "universal":
            return ((self.a * key + self.b) % self.p) % self.size
    
    def insert(self, value: Data, key=None):
        '''Inserts a key-value pair into the hash table. 
        Average: O(1), Worst-case: O(n) due to collisions.'''

        iterations = 1

        if key is None:
            key = value.salary

        index = self._hash(key)
        bucket = self.table[index]

        if not bucket:
            self.table[index] = [[key, value]]
            self.ocupation += 1
            return iterations

        # Handle collision: check if key already exists
        for i, (k, v) in enumerate(bucket):
            iterations += 1
            if k == key:
                # Update existing value
                bucket[i][1] = value
                return iterations

        # If key does not exist, append new pair
        bucket.append([key, value])

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


    def delete(self, key):
        '''Deletes the key-value pair associated with the given key. complexity: O(1) on average, O(n) in worst case due to collisions.'''

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
    