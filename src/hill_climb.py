import random
import math


def generate_initial_solution(weights, n, capacity):
    initial_solution = [random.choice([0, 1]) for _ in range(n)]

    total_weight = sum(weights[i] for i in range(n) if initial_solution[i] == 1)
    included_idx = [i for i in range(n) if initial_solution[i] == 1]

    while total_weight > capacity:
        idx = random.choice(included_idx)
        included_idx.remove(idx)
        initial_solution[idx] = 0
        total_weight -= weights[idx]

    return initial_solution


def simulated_annealing(weights, vals, n, capacity, initial_solution):
    def evaluate(solution):
        sum_weights = sum(weights[i] if solution[i] == 1 else 0 for i in range(n))
        sum_vals = sum(vals[i] if solution[i] == 1 else 0 for i in range(n))

        if sum_weights > capacity:
            return -1
        return sum_vals

    def generate_neighbor(solution):
        neighbor = solution[:]
        current_weight = sum(
            weights[i] if solution[i] == 1 else 0 for i in range(len(solution))
        )

        if random.random() < 0.5:  # Try to add an item
            # Only consider items that could fit
            potential_adds = [
                i
                for i in range(len(solution))
                if solution[i] == 0 and current_weight + weights[i] <= capacity
            ]
            if potential_adds:
                idx = random.choice(potential_adds)
                neighbor[idx] = 1
        else:  # Remove an item
            selected = [i for i in range(len(solution)) if solution[i] == 1]
            if selected:
                idx = random.choice(selected)
                neighbor[idx] = 0

        return neighbor

    # Initial temperature and cooling rate
    temp = 1000.0
    cooling_rate = 0.95
    min_temp = 0.1

    current_solution = initial_solution
    current_value = evaluate(current_solution)

    best_solution = current_solution[:]
    best_value = current_value

    while temp > min_temp:
        neighbor = generate_neighbor(current_solution)

        score = evaluate(neighbor)

        delta = score - current_value

        # if the neighbor is better, accpet it
        # if it's worse, accpet it with a certain probability
        if delta > 0 or random.random() < math.exp(delta / temp):
            current_solution = neighbor
            current_value = score

            if current_value > best_value:
                best_value = current_value
                best_solution = current_solution[:]

        temp *= cooling_rate

    selected_indices = [i for i in range(n) if best_solution[i]]

    return best_value, selected_indices
