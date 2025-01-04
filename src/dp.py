"""
"""


def top_down(weights, vals, n, g, memo):
    if n == 0 or g == 0:
        return 0, []

    if memo[n][g][0] != -1 and memo[n][g][1] != []:
        return memo[n][g]

    if weights[n - 1] > g:
        memo[n][g] = top_down(weights, vals, n - 1, g, memo)
        return memo[n][g]

    rez_1, sol_1 = top_down(weights, vals, n - 1, g, memo)
    rez_2, sol_2 = top_down(weights, vals, n - 1, g - weights[n - 1], memo)

    if rez_1 > rez_2 + vals[n - 1]:
        memo[n][g] = rez_1, sol_1
        return memo[n][g]

    memo[n][g] = rez_2 + vals[n - 1], sol_2 + [n - 1]
    return memo[n][g]


def bottom_up(weights, vals, n, g):
    dp = [[0 for _ in range(g + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, g + 1):
            if weights[i - 1] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(
                    dp[i - 1][j], dp[i - 1][j - weights[i - 1]] + vals[i - 1]
                )

    rez = dp[n][g]

    sol = []
    for i in range(n, 0, -1):
        if dp[i][g] != dp[i - 1][g]:
            sol.append(i - 1)
            g -= weights[i - 1]

    return rez, sol[::-1]
