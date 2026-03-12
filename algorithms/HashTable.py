class HashTable:
    '''Implements a hash table data structure using separate chaining for collision resolution.'''
    
    def __init__(self, size, hash_type='modular'):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.hash_type = hash_type

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
    
    def insert(self, key, value):
        '''Inserts a key-value pair into the hash table. complexity: O(1) on average, O(n) in worst case due to collisions.'''
        key = value
        index = self._hash(key)

        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
            
        self.table[index].append([key, value])
    
    def get(self, key):
        '''Retrieves the value associated with the given key. complexity: O(1) on average, O(n) in worst case due to collisions.'''

        index = self._hash(key)

        for k, v in self.table[index]:
            if k == key:
                return v

        return None
    
    def delete(self, key):
        '''Deletes the key-value pair associated with the given key. complexity: O(1) on average, O(n) in worst case due to collisions.'''

        index = self._hash(key)

        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True

        return False

    def display(self):
        for i, bucket in enumerate(self.table):
            print(f"{i}: {bucket}")