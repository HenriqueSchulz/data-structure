import random
import string
from data import Data

class DataGenerator:
    '''Implements a generator of Data Objects'''

    @staticmethod
    def generate(size):
        data_list = []

        for i in range(size):
            name = ''.join(random.choices(string.ascii_letters, k=8))
            salary = random.randint(1000, 40000)

            data = Data(name, salary, i)
            data_list.append(data)

        return data_list
