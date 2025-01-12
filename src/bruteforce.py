"""
    This file contains the brute force solution to the knapsack problem.
    The brute force solution is a recursive solution that tries all possible
    combinations of items in the knapsack and returns the maximum value that
    can be obtained without exceeding the weight limit.
"""

def brute_force(weights, vals, n, g):
    if n == 0 or g == 0:
        return 0, []

    if weights[n - 1] > g:
        return brute_force(weights, vals, n - 1, g)

    rez_1, sol_1 = brute_force(weights, vals, n - 1, g)
    rez_2, sol_2 = brute_force(weights, vals, n - 1, g - weights[n - 1])

    if rez_1 > rez_2 + vals[n - 1]:
        return rez_1, sol_1
    return rez_2 + vals[n - 1], sol_2 + [n - 1]
