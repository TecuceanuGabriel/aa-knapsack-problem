from tests.generate_tests import generate_tests, test_sizes, scenarios, capacities

from src.bruteforce import brute_force
from src.dp import top_down, bottom_up
from src.greedy import greedy_helper, GreedyHeuristic
from src.branch_bound import branch_and_bound
from src.hill_climb import (
    generate_initial_solution,
    simulated_annealing,
)

from src.data_point import DataPoint

import timeit
import time
import os
import sys
import math
import signal
import json

sys.setrecursionlimit(10**6)

NR_RUNS = 10

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Timed out")

signal.signal(signal.SIGALRM, timeout_handler)

Data = {}

def run_test():
    test_nr = 0
    Data = {}

    for c in capacities:
        Data[c] = {}
        for s in scenarios:
            Data[c][s] = {}

            Data[c][s]["bf"] = []
            Data[c][s]["dp_td"] = []
            Data[c][s]["dp_bu"] = []
            Data[c][s]["bb"] = []

            Data[c][s]["greedy_r"] = []
            Data[c][s]["greedy_s"] = []
            Data[c][s]["greedy_v"] = []
            Data[c][s]["greedy_w"] = []

            Data[c][s]["sa"] = []            

            for n in test_sizes:
                # Open the test case file and read data
                with open(f"tests/in/test_{test_nr}_{c}_{s}_n{n}.in", "r") as f:
                    n, capacity = map(int, f.readline().split())
                    weights = []
                    vals = []

                    for _ in range(n):
                        w, v = map(int, f.readline().split())
                        weights.append(w)
                        vals.append(v)

                print(f"test {test_nr}, {c}/{s}/{n}")

                # Run algorithms and store results
                if n <= 20:
                    bf_result = run_brute_force(weights, vals, n, capacity, test_nr)
                    Data[c][s]["bf"].append(bf_result.toJSON())
                else:
                    print("brute force: skipped")

                dp_td_result = run_dp_top_down(weights, vals, n, capacity, test_nr)
                Data[c][s]["dp_td"].append(dp_td_result.toJSON())

                dp_bu_rez, dp_bu_point = run_dp_bottom_up(weights, vals, n, capacity, test_nr)
                Data[c][s]["dp_bu"].append(dp_bu_point.toJSON())

                bb_rez, bb_point = run_branch_bound(weights, vals, n, capacity, test_nr)
                Data[c][s]["bb"].append(bb_point.toJSON())

                real_rez = dp_bu_rez if dp_bu_rez != -1 else bb_rez

                greedy_r_result = run_greedy_ratio(weights, vals, n, capacity, test_nr, real_rez)
                Data[c][s]["greedy_r"].append(greedy_r_result.toJSON())

                greedy_s_result = run_greedy_stats(weights, vals, n, capacity, test_nr, real_rez)
                Data[c][s]["greedy_s"].append(greedy_s_result.toJSON())

                greedy_v_result = run_greedy_value(weights, vals, n, capacity, test_nr, real_rez)
                Data[c][s]["greedy_v"].append(greedy_v_result.toJSON())

                greedy_w_result = run_greedy_weight(weights, vals, n, capacity, test_nr, real_rez)
                Data[c][s]["greedy_w"].append(greedy_w_result.toJSON())

                sa_result = run_simulated_anneling(weights, vals, n, capacity, test_nr, real_rez)
                Data[c][s]["sa"].append(sa_result.toJSON())

                print()

                test_nr += 1

    f = open("tests/out/data.json", "w")
    json.dump(Data, f, indent=4)



def run_brute_force(weights, vals, n, capacity, i):
    os.makedirs("tests/out/bf", exist_ok=True)

    f = open(f"tests/out/bf/test{i}.out", "w")

    rez, sol = brute_force(weights, vals, n, capacity)

    time = timeit.timeit(
        lambda: brute_force(weights, vals, n, capacity), number=NR_RUNS
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    duration = time / NR_RUNS

    print(f"brute force time: {duration}")

    f.close()

    return DataPoint(n, capacity, duration, 100)


def top_down_wrapper(weights, vals, n, capacity):
    memo = [[(-1, []) for _ in range(capacity + 1)] for _ in range(n + 1)]
    return top_down(weights, vals, n, capacity, memo)


def run_dp_top_down(weights, vals, n, capacity, i):
    os.makedirs("tests/out/dp_td", exist_ok=True)

    f = open(f"tests/out/dp_td/test{i}.out", "w")

    try:
        signal.alarm(40)
        rez, sol = top_down_wrapper(weights, vals, n, capacity)
        signal.alarm(0)
    except TimeoutException:
        print("dp top down: timeout")
        return DataPoint(n, capacity, math.inf, 0)

    time = timeit.timeit(
        lambda: top_down_wrapper(weights, vals, n, capacity), number=NR_RUNS
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    duration = time / NR_RUNS

    print(f"dp top down time: {duration}")

    f.close()

    return DataPoint(n, capacity, duration, 100)


def run_dp_bottom_up(weights, vals, n, capacity, i):
    os.makedirs("tests/out/dp_bu", exist_ok=True)

    f = open(f"tests/out/dp_bu/test{i}.out", "w")

    try:
        signal.alarm(40)
        rez, sol = bottom_up(weights, vals, n, capacity)
        signal.alarm(0)
    except TimeoutException:
        print("dp bottom up: timeout")
        return -1, DataPoint(n, capacity, math.inf, 0)

    time = timeit.timeit(lambda: bottom_up(weights, vals, n, capacity), number=NR_RUNS)

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    duration = time / NR_RUNS

    print(f"dp bottom up time: {duration}")

    f.close()

    return rez, DataPoint(n, capacity, duration, 100)


def run_greedy_ratio(weights, vals, n, capacity, i, real_rez):
    os.makedirs("tests/out/greedy_r", exist_ok=True)

    f = open(f"tests/out/greedy_r/test{i}.out", "w")

    rez, sol = greedy_helper(weights, vals, n, capacity, GreedyHeuristic.RATIO)

    time = timeit.timeit(
        lambda: greedy_helper(weights, vals, n, capacity, GreedyHeuristic.RATIO),
        number=NR_RUNS,
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    duration = time / NR_RUNS
    accuracy = rez / real_rez * 100

    print(
        "greedy ratio:",
        f"time: {duration}",
        f"accuracy: {accuracy}%",
        sep="\n",
    )

    print()

    f.close()

    return DataPoint(n, capacity, duration, accuracy)


def run_greedy_weight(weights, vals, n, capacity, i, real_rez):
    os.makedirs("tests/out/greedy_w", exist_ok=True)

    f = open(f"tests/out/greedy_w/test{i}.out", "w")

    rez, sol = greedy_helper(weights, vals, n, capacity, GreedyHeuristic.WEIGHT)

    time = timeit.timeit(
        lambda: greedy_helper(weights, vals, n, capacity, GreedyHeuristic.WEIGHT),
        number=NR_RUNS,
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    duration = time / NR_RUNS
    accuracy = rez / real_rez * 100

    print(
        "greedy weight:",
        f"time: {duration}",
        f"accuracy: {accuracy}%",
        sep="\n",
    )

    print()

    f.close()

    return DataPoint(n, capacity, duration, accuracy)


def run_greedy_value(weights, vals, n, capacity, i, real_rez):
    os.makedirs("tests/out/greedy_v", exist_ok=True)

    f = open(f"tests/out/greedy_v/test{i}.out", "w")

    rez, sol = greedy_helper(weights, vals, n, capacity, GreedyHeuristic.VALUE)

    time = timeit.timeit(
        lambda: greedy_helper(weights, vals, n, capacity, GreedyHeuristic.VALUE),
        number=NR_RUNS,
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    duration = time / NR_RUNS
    accuracy = rez / real_rez * 100

    print(
        "greedy value:",
        f"time: {duration}",
        f"accuracy: {accuracy}%",
        sep="\n",
    )

    print()

    f.close()

    return DataPoint(n, capacity, duration, accuracy)


def run_greedy_stats(weights, vals, n, capacity, i, real_rez):
    os.makedirs("tests/out/greedy_s", exist_ok=True)

    f = open(f"tests/out/greedy_s/test{i}.out", "w")

    rez, sol = greedy_helper(weights, vals, n, capacity, GreedyHeuristic.STATS)

    time = timeit.timeit(
        lambda: greedy_helper(weights, vals, n, capacity, GreedyHeuristic.STATS),
        number=NR_RUNS,
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    duration = time / NR_RUNS
    accuracy = rez / real_rez * 100

    print(
        "greedy stats:",
        f"time: {duration}",
        f"accuracy: {accuracy}%",
        sep="\n",
    )

    print()

    f.close()

    return DataPoint(n, capacity, duration, accuracy)


def run_branch_bound(weights, vals, n, capacity, i):
    os.makedirs("tests/out/bb", exist_ok=True)

    f = open(f"tests/out/bb/test{i}.out", "w")

    try:
        signal.alarm(40)
        rez, sol = branch_and_bound(weights, vals, n, capacity)
        signal.alarm(0)
    except TimeoutException:
        print("branch and bound: timeout")
        return -1, DataPoint(n, capacity, math.inf, 0)

    time = timeit.timeit(
        lambda: branch_and_bound(weights, vals, n, capacity), number=NR_RUNS
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    duration = time / NR_RUNS

    print(f"branch and bound time: {duration}")

    print()

    f.close()

    return rez, DataPoint(n, capacity, duration, 100)


def run_simulated_anneling(weights, vals, n, capacity, i, real_rez):
    os.makedirs("tests/out/sa", exist_ok=True)

    f = open(f"tests/out/sa/test{i}.out", "w")

    initial_solution = generate_initial_solution(weights, n, capacity)

    rez, sol = simulated_annealing(weights, vals, n, capacity, initial_solution)

    time = timeit.timeit(
        lambda: simulated_annealing(weights, vals, n, capacity, initial_solution),
        number=NR_RUNS,
    )

    f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

    duration = time / NR_RUNS
    accuracy = rez / real_rez * 100

    print(
        "simulated annealing:",
        f"time: {duration}",
        f"accuracy: {accuracy}%",
        sep="\n",
    )

    print()

    f.close()

    return DataPoint(n, capacity, duration, accuracy)


if __name__ == "__main__":
    generate_tests()

    start = time.perf_counter()
    run_test()
    end = time.perf_counter()

    print(f"total time: {(end - start)/60} minutes")
