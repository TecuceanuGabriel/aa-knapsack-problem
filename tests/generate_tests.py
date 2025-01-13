import random
import os
import math

test_sizes = [20, 100, 250, 500, 750, 1000, 3000, 5000, 8000, 10000]


capacities = ["low", "medium", "high"]

scenarios = [
    "random",
    "uniform",
    "high_value_weight_ratio",
    "low_value_weight_ratio",
]

magnitude = 100


def generate_tests():
    test_nr = 0

    for c in capacities:
        for s in scenarios:
            for n in test_sizes:
                vals = []
                weights = []

                if s == "random":
                    for _ in range(n):
                        vals.append(random.randint(1, magnitude))
                        weights.append(random.randint(1, magnitude))

                elif s == "uniform":
                    val = random.randint(int(magnitude / 10), magnitude)

                    var = int(val * 0.1)

                    for _ in range(n):
                        vals.append(random.randint(val - var, val + var))
                        weights.append(random.randint(val - var, val + var))

                elif s == "low_value_weight_ratio":
                    for _ in range(n):
                        val = random.randint(int(magnitude / 10), magnitude)
                        weight = random.randint(2, 7) * val

                        vals.append(val)
                        weights.append(weight)

                elif s == "high_value_weight_ratio":
                    for _ in range(n):
                        weight = random.randint(int(magnitude / 10), magnitude)
                        val = random.randint(2, 7) * weight

                        vals.append(val)
                        weights.append(weight)

                if c == "low":
                    cap = 0.1
                elif c == "medium":
                    cap = 0.3
                else:
                    cap = 0.5

                if n > 100:
                    cap = int(cap * sum(weights) * 1 / math.sqrt(n))
                else:
                    cap = int(cap * sum(weights))

                os.makedirs(f"tests/in", exist_ok=True)

                f = open(f"tests/in/test_{test_nr}_{c}_{s}_n{n}.in", "w")

                f.write(f"{n} {cap}\n")

                for i in range(n):
                    f.write(f"{weights[i]} {vals[i]}\n")

                f.close()

                test_nr += 1
