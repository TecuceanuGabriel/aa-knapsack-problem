import random


def hill_climb(weights, vals, n, capacity):
    def evaluate(solution):
        sum_weights = sum(weights[i] if solution[i] == 1 else 0 for i in range(n))
        sum_vals = sum(vals[i] if solution[i] == 1 else 0 for i in range(n))

        if sum_weights > capacity:
            return -1
        return sum_vals

    def get_neighbors(solution):
        neighbors = []

        for i in range(n):
            neighbor = solution[:]
            neighbor[i] = 1 - neighbor[i]
            neighbors.append(neighbor)

        return neighbors

    initial_solution = [random.choice([0, 1]) for _ in range(n)]
    total_weight = sum(weights[i] for i in range(n) if initial_solution[i] == 1)
    included_idx = [i for i in range(n) if initial_solution[i] == 1]
    while total_weight > capacity:
        idx = random.choice(included_idx)
        included_idx.remove(idx)
        initial_solution[idx] = 0
        total_weight -= weights[idx]

    current_solution = initial_solution
    current_score = evaluate(current_solution)

    iter = 0

    while True:
        iter += 1

        neighbors = get_neighbors(current_solution)
        best_neighbor = max(neighbors, key=evaluate)
        best_score = evaluate(best_neighbor)

        if best_score <= current_score:  # no improvement
            break

        current_solution = best_neighbor
        current_score = best_score

    included_idx = [i for i in range(n) if current_solution[i] == 1]

    return current_score, included_idx, iter


def random_restart_hill_climb(weights, vals, n, capacity, num_restarts):
    best_score = -1
    best_solution = []
    best_iter = 0

    for _ in range(num_restarts):
        score, solution, iter = hill_climb(weights, vals, n, capacity)

        if score > best_score:
            best_score = score
            best_solution = solution
            best_iter = iter

    return best_score, best_solution, best_iter
