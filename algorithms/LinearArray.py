class LinearArray:
    '''Implements a linear array data structure.'''

    def __init__(self, size):
        self.size = size
        self.occupation = 0
        self.array = [None] * size

    def insert(self, value):
        '''Inserts a value at any available index in the array. complexity: O(1)'''

        if self.occupation >= self.size:
            raise IndexError("Array is full")

        self.array[self.occupation] = value
        self.occupation += 1

    def delete(self, index):
        '''Deletes the value at the specified index. complexity: O(n)'''

        if index < 0 or index >= self.occupation:
            raise IndexError("Index out of bounds")

        for i in range(index, self.occupation - 1):
            self.array[i] = self.array[i + 1]

        self.array[self.occupation - 1] = None
        self.occupation -= 1

    def get(self, index):
        '''Retrieves the value at the specified index. complexity: O(1)'''

        if index < 0 or index >= self.occupation:
            raise IndexError("Index out of bounds")
        
        return self.array[index]

    def display(self):
        for i in range(self.size):
            print(f"Index {i}: {self.array[i]}")