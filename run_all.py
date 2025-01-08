from tests.generate_tests import generate_tests

from src.bruteforce import brute_force
from src.dp import top_down, bottom_up
from src.greedy import greedy_helper, GreedyHeuristic
from src.branch_bound import branch_and_bound
from src.hill_climb import (
    hill_climb,
    random_restart_hill_climb,
    generate_initial_solution,
)

import timeit
import os

NR_RUNS = 10


def run_test():
    for i in range(5):
        # read
        f = open(f"tests/in/test{i}.in", "r")

        n, capacity = map(int, f.readline().split())

        print(n, capacity)

        weights = []
        vals = []

        for _ in range(n):
            w, v = map(int, f.readline().split())
            weights.append(w)
            vals.append(v)

        f.close()

        print(f"Test {i}:")

        # write
        run_brute_force(weights, vals, n, capacity, i)
        run_dp_top_down(weights, vals, n, capacity, i)
        run_dp_bottom_up(weights, vals, n, capacity, i)
        run_greedy(weights, vals, n, capacity, i)
        run_branch_bound(weights, vals, n, capacity, i)
        run_hill_climb(weights, vals, n, capacity, i)
        run_random_restart_hill_climb(weights, vals, n, capacity, i)

        print()


def run_brute_force(weights, vals, n, capacity, i):
    os.makedirs("tests/out/bf", exist_ok=True)

    f = open(f"tests/out/bf/test{i}.out", "w")

    rez, sol = brute_force(weights, vals, n, capacity)

    time = timeit.timeit(
        lambda: brute_force(weights, vals, n, capacity), number=NR_RUNS
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    print(f"brute force time: {time / NR_RUNS}")

    f.close()


def top_down_wrapper(weights, vals, n, capacity):
    memo = [[(-1, []) for _ in range(capacity + 1)] for _ in range(n + 1)]
    return top_down(weights, vals, n, capacity, memo)


def run_dp_top_down(weights, vals, n, capacity, i):
    os.makedirs("tests/out/dp_td", exist_ok=True)

    f = open(f"tests/out/dp_td/test{i}.out", "w")

    rez, sol = top_down_wrapper(weights, vals, n, capacity)

    time = timeit.timeit(
        lambda: top_down_wrapper(weights, vals, n, capacity), number=NR_RUNS
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    print(f"dp top down time: {time / NR_RUNS}")

    f.close()


def run_dp_bottom_up(weights, vals, n, capacity, i):
    os.makedirs("tests/out/dp_bu", exist_ok=True)

    f = open(f"tests/out/dp_bu/test{i}.out", "w")

    rez, sol = bottom_up(weights, vals, n, capacity)

    time = timeit.timeit(lambda: bottom_up(weights, vals, n, capacity), number=NR_RUNS)

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    print(f"dp bottom up time: {time / NR_RUNS}")

    f.close()


def run_greedy(weights, vals, n, capacity, i):
    run_greedy_ratio(weights, vals, n, capacity, i)
    run_greedy_weight(weights, vals, n, capacity, i)
    run_greedy_value(weights, vals, n, capacity, i)
    run_greedy_stats(weights, vals, n, capacity, i)


def run_greedy_ratio(weights, vals, n, capacity, i):
    os.makedirs("tests/out/greedy_r", exist_ok=True)

    f = open(f"tests/out/greedy_r/test{i}.out", "w")

    real_rez, _ = brute_force(weights, vals, n, capacity)

    rez, sol = greedy_helper(weights, vals, n, capacity, GreedyHeuristic.RATIO)

    time = timeit.timeit(
        lambda: greedy_helper(weights, vals, n, capacity, GreedyHeuristic.RATIO),
        number=NR_RUNS,
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    print(
        "greedy ratio:",
        f"time: {time / NR_RUNS}",
        f"accuracy: {rez / real_rez * 100}%",
        sep="\n",
    )

    print()

    f.close()


def run_greedy_weight(weights, vals, n, capacity, i):
    os.makedirs("tests/out/greedy_w", exist_ok=True)

    f = open(f"tests/out/greedy_w/test{i}.out", "w")

    real_rez, _ = brute_force(weights, vals, n, capacity)

    rez, sol = greedy_helper(weights, vals, n, capacity, GreedyHeuristic.WEIGHT)

    time = timeit.timeit(
        lambda: greedy_helper(weights, vals, n, capacity, GreedyHeuristic.WEIGHT),
        number=NR_RUNS,
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    print(
        "greedy weight:",
        f"time: {time / NR_RUNS}",
        f"accuracy: {rez / real_rez * 100}%",
        sep="\n",
    )

    print()

    f.close()


def run_greedy_value(weights, vals, n, capacity, i):
    os.makedirs("tests/out/greedy_v", exist_ok=True)

    f = open(f"tests/out/greedy_v/test{i}.out", "w")

    real_rez, _ = brute_force(weights, vals, n, capacity)

    rez, sol = greedy_helper(weights, vals, n, capacity, GreedyHeuristic.VALUE)

    time = timeit.timeit(
        lambda: greedy_helper(weights, vals, n, capacity, GreedyHeuristic.VALUE),
        number=NR_RUNS,
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    print(
        "greedy value:",
        f"time: {time / NR_RUNS}",
        f"accuracy: {rez / real_rez * 100}%",
        sep="\n",
    )

    print()

    f.close()


def run_greedy_stats(weights, vals, n, capacity, i):
    os.makedirs("tests/out/greedy_s", exist_ok=True)

    f = open(f"tests/out/greedy_s/test{i}.out", "w")

    real_rez, _ = brute_force(weights, vals, n, capacity)

    rez, sol = greedy_helper(weights, vals, n, capacity, GreedyHeuristic.STATS)

    time = timeit.timeit(
        lambda: greedy_helper(weights, vals, n, capacity, GreedyHeuristic.STATS),
        number=NR_RUNS,
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    print(
        "greedy stats:",
        f"time: {time / NR_RUNS}",
        f"accuracy: {rez / real_rez * 100}%",
        sep="\n",
    )

    print()

    f.close()


def run_branch_bound(weights, vals, n, capacity, i):
    os.makedirs("tests/out/bb", exist_ok=True)

    f = open(f"tests/out/bb/test{i}.out", "w")

    rez, sol = branch_and_bound(weights, vals, n, capacity)

    time = timeit.timeit(
        lambda: branch_and_bound(weights, vals, n, capacity), number=NR_RUNS
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    print(f"branch and bound time: {time / NR_RUNS}")

    print()

    f.close()


def run_hill_climb(weights, vals, n, capacity, i):
    os.makedirs("tests/out/hc", exist_ok=True)

    f = open(f"tests/out/hc/test{i}.out", "w")

    real_rez, _ = brute_force(weights, vals, n, capacity)

    initial_solution = generate_initial_solution(weights, n, capacity)

    rez, sol, iter = hill_climb(weights, vals, n, capacity, initial_solution)

    time = timeit.timeit(
        lambda: hill_climb(weights, vals, n, capacity, initial_solution), number=NR_RUNS
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    print(
        "hill climb:",
        f"time: {time / NR_RUNS}",
        f"accuracy: {rez / real_rez * 100}%",
        f"nr of iterations: {iter}",
        sep="\n",
    )

    print()

    f.close()


NR_RESTARTS = 100


def run_random_restart_hill_climb(weights, vals, n, capacity, i):
    os.makedirs("tests/out/rrhc", exist_ok=True)

    f = open(f"tests/out/rrhc/test{i}.out", "w")

    real_rez, _ = brute_force(weights, vals, n, capacity)

    initial_solutions = [
        generate_initial_solution(weights, n, capacity) for _ in range(NR_RESTARTS)
    ]

    rez, sol, iter = random_restart_hill_climb(
        weights, vals, n, capacity, NR_RESTARTS, initial_solutions
    )

    time = timeit.timeit(
        lambda: random_restart_hill_climb(
            weights, vals, n, capacity, NR_RESTARTS, initial_solutions
        ),
        number=NR_RUNS,
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    print(
        f"random restart hill climb ({NR_RESTARTS}):",
        f"time: {time / NR_RUNS}",
        f"accuracy: {rez / real_rez * 100}%",
        f"best nr of iterations: {iter}",
        sep="\n",
    )

    f.close()


if __name__ == "__main__":
    generate_tests()
    run_test()
