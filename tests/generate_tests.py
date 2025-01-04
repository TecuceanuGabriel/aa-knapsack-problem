import random

def generate_tests():
    n = 20

    for i in range(5):
        weights = []
        vals = []

        for _ in range(n):
            weights.append(random.randint(1, 100))
            vals.append(random.randint(1, 100))

        f = open(f'tests/test{i}.in', 'w')

        f.write(f'{n} {random.randint(1, 1000)} \n')

        for j in range(n):
            f.write(f'{weights[j]} {vals[j]} \n')

        f.close()

