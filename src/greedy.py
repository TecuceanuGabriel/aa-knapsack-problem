def greedy_ratio(weights, vals, n, g):
    arr = [(vals[i] / weights[i], i) for i in range(n)]
    arr.sort(reverse=True)

    rez = 0
    sol = []

    for i in range(n):
        if weights[arr[i][1]] <= g:
            rez += vals[arr[i][1]]
            g -= weights[arr[i][1]]
            sol.append(arr[i][1])
        else:
            break

    return rez, sol


def greedy_weight(weights, vals, n, g):
    arr = [(weights[i], i) for i in range(n)]
    arr.sort()

    rez = 0
    sol = []

    for i in range(n):
        if weights[arr[i][1]] <= g:
            rez += vals[arr[i][1]]
            g -= arr[i][0]
            sol.append(arr[i][1])
        else:
            break

    return rez, sol


def greedy_value(weights, vals, n, g):
    arr = [(vals[i], i) for i in range(n)]
    arr.sort(reverse=True)

    rez = 0
    sol = []

    for i in range(n):
        if weights[arr[i][1]] <= g:
            rez += arr[i][0]
            g -= weights[arr[i][1]]
            sol.append(arr[i][1])
        else:
            break

    return rez, sol
