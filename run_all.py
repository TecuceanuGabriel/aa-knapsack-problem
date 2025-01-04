from tests.generate_tests import generate_tests

from src.bruteforce import brute_force
from src.dp import top_down, bottom_up
from src.greedy import greedy_ratio, greedy_weight, greedy_value


def run_test():
    for i in range(5):
        # read
        f = open(f"tests/test{i}.in", "r")

        n, g = map(int, f.readline().split())

        print(n, g)

        weights = []
        vals = []

        for _ in range(n):
            w, v = map(int, f.readline().split())
            weights.append(w)
            vals.append(v)

        f.close()

        # write
        f = open(f"tests/bt/test{i}.out", "w")

        rez, sol = brute_force(weights, vals, n, g)
        f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

        f.close()

        f = open(f"tests/dp/test{i}.out", "w")

        memo = [[(-1, []) for _ in range(g + 1)] for _ in range(n + 1)]
        rez, sol = top_down(weights, vals, n, g, memo)

        f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

        f = open(f"tests/dp_bu/test{i}.out", "w")

        rez, sol = bottom_up(weights, vals, n, g)
        f.write(f"{rez}\n" f"{' '.join(map(str, sol))}\n")

        f.close()

        run_greedy(weights, vals, n, g, i)


def run_greedy(weights, vals, n, g, i):
    f = open(f"tests/greedy/test{i}.out", "w")

    real_rez, _ = brute_force(weights, vals, n, g)

    ratio_ans = greedy_ratio(weights, vals, n, g)
    weight_ans = greedy_weight(weights, vals, n, g)
    value_ans = greedy_value(weights, vals, n, g)

    best_ans = max(ratio_ans, weight_ans, value_ans)

    f.write(f"{best_ans[0]}\n" f"{' '.join(map(str, best_ans[1]))}\n")

    print(
        f"diff: {real_rez - best_ans[0]}",
        best_ans[0],
        real_rez,
        f"{float(best_ans[0]) / float(real_rez) * 100}%",
    )

    f.close()


if __name__ == "__main__":
    generate_tests()
    run_test()
