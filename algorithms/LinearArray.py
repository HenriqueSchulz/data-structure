from data import Data

class LinearArray:
    '''Implements a linear array data structure.'''

    def __init__(self, size):
        self.size = size
        self.occupation = 0
        self.array: list[Data] = [None] * size

    def insert(self, value: Data):
        '''Inserts a value at any available index in the array. complexity: O(1)'''

        if self.occupation >= self.size:
            raise IndexError("Array is full")

        self.array[self.occupation] = value
        self.occupation += 1

        iterations = 1
        return iterations   

    def delete(self, index):
        '''Deletes the value at the specified index. complexity: O(n)'''

        if index < 0 or index >= self.occupation:
            raise IndexError("Index out of bounds")

        for i in range(index, self.occupation - 1):
            self.array[i] = self.array[i + 1]

        self.array[self.occupation - 1] = None
        self.occupation -= 1

    def get_by_index(self, index):
        '''Retrieves the value at the specified index. complexity: O(1)'''

        if index < 0 or index >= self.occupation:
            raise IndexError("Index out of bounds")
        
        return self.array[index]
    
    def get(self, key):
        '''Searches for a value by key (salary). Complexity: O(n)'''

        iterations = 0

        for i in range(self.occupation):

            iterations += 1

            if self.array[i].salary == key:
                return self.array[i], iterations

        return None, iterations

    def display(self):
        for i in range(self.size):
            print(f"Index {i}: {self.array[i]}")