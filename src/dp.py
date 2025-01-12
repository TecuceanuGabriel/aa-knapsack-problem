"""
"""


def top_down(weights, vals, n, capacity, memo):
    if n == 0 or capacity == 0:
        return 0, []

    if memo[n][capacity] != (-1, []):
        return memo[n][capacity]

    if weights[n - 1] > capacity:
        memo[n][capacity] = top_down(weights, vals, n - 1, capacity, memo)
        return memo[n][capacity]

    rez_1, sol_1 = top_down(weights, vals, n - 1, capacity, memo)
    rez_2, sol_2 = top_down(weights, vals, n - 1, capacity - weights[n - 1], memo)

    if rez_1 > rez_2 + vals[n - 1]:
        memo[n][capacity] = rez_1, sol_1
        return memo[n][capacity]

    memo[n][capacity] = rez_2 + vals[n - 1], sol_2 + [n - 1]
    return memo[n][capacity]


def bottom_up(weights, vals, n, capacity):
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            if weights[i - 1] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(
                    dp[i - 1][j], dp[i - 1][j - weights[i - 1]] + vals[i - 1]
                )

    rez = dp[n][capacity]

    sol = []
    for i in range(n, 0, -1):
        if dp[i][capacity] != dp[i - 1][capacity]:
            sol.append(i - 1)
            capacity -= weights[i - 1]

    return rez, sol[::-1]
