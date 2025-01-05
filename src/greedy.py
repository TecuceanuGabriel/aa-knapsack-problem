from enum import Enum


class GreedyHeuristic(Enum):
    RATIO = 0
    WEIGHT = 1
    VALUE = 2
    STATS = 3


def greedy_helper(weight, vals, n, capacity, heuristic):
    # combine the two lists into a list of tuples
    items = zip(weight, vals)

    if heuristic == GreedyHeuristic.RATIO:
        items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)
    elif heuristic == GreedyHeuristic.WEIGHT:
        items = sorted(items, key=lambda x: x[0], reverse=True)
    elif heuristic == GreedyHeuristic.VALUE:
        items = sorted(items, key=lambda x: x[1], reverse=True)
    elif heuristic == GreedyHeuristic.STATS:
        a, b = get_coeff(weight, vals, n, capacity)
        items = sorted(items, key=lambda x: a * x[1] - b * x[0], reverse=True)

    # get the two lists back
    weights, vals = zip(*items)

    return greedy(weights, vals, n, capacity)


def get_coeff(weights, vals, n, capacity):
    # normalize the weights and values
    w_max = max(weights)
    w_min = min(weights)
    weights = [(w - w_min) / (w_max - w_min) for w in weights]

    v_max = max(vals)
    v_min = min(vals)
    vals = [(v - v_min) / (v_max - v_min) for v in vals]

    # calculate the variance coefficients
    sum_w = sum(weights)
    sum_v = sum(vals)

    mean_w = sum_w / n
    mean_v = sum_v / n

    dev_w = sum([(w - mean_w) ** 2 for w in weights]) / n
    dev_v = sum([(v - mean_v) ** 2 for v in vals]) / n

    cv_w = dev_w / mean_w
    cv_v = dev_v / mean_v

    # assign a higher coefficient to the factor with greater relative variation
    a = cv_v / (cv_w + cv_v)
    b = cv_w / (cv_w + cv_v)

    # if the capacity is too small, adjust the coefficients
    if capacity / sum_w < 1e-4:
        b = b * sum_w / capacity
        a = 1 - b

    return a, b


def greedy(weights, vals, n, capacity):
    rez = 0
    sol = []

    for i in range(n):
        if weights[i] <= capacity:
            rez += vals[i]
            capacity -= weights[i]
            sol.append(i)
        else:
            break

    return rez, sol
