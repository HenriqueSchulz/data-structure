import random
from datetime import datetime, timedelta
from .Data import Data

class DataGenerator:

    DEPARTMENTS = ["IT", "HR", "Finance", "Sales", "Marketing"]
    CITIES = ["SP", "RJ", "Curitiba", "Porto Alegre", "BH"]
    NAMES = ["Ana", "João", "Maria", "Pedro", "Lucas", "Fernanda"]

    @staticmethod
    def generate(size):
        data_list = []

        for i in range(size):
            age = random.randint(18, 65)

            experience = max(0, age - 18 - random.randint(0, 5))

            # salário correlacionado com experiência
            salary = int(random.gauss(3000 + experience * 500, 1500))
            salary = max(1200, salary)

            performance = min(10, max(0, random.gauss(7, 2)))

            join_date = datetime.now() - timedelta(days=random.randint(0, 3650))

            data = Data(
                id=random.randint(0, size * 10),
                name=random.choice(DataGenerator.NAMES),
                age=age,
                salary=salary,
                department=random.choice(DataGenerator.DEPARTMENTS),
                city=random.choice(DataGenerator.CITIES),
                experience_years=experience,
                performance_score=round(performance, 2),
                join_date=join_date,
                is_active=random.random() > 0.1
            )

            data_list.append(data)

        return data_list