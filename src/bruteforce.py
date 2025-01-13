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
