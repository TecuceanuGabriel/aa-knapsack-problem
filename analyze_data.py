from tests.generate_tests import test_sizes, scenarios, capacities

from src.data_point import DataPoint

import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import seaborn as sns

matplotlib.use('Qt5Agg')

Data = {}

def do_analysis():
    f = open("tests/out/data.json", "r")
    Data = json.load(f)
    f.close()

    fig_nr = 0

    for c in capacities:
        for s in scenarios:
            data = Data[c][s]

            dp_td = [DataPoint(d["n"], d["time"], d["accuracy"]) for d in data["dp_td"]]
            dp_bu = [DataPoint(d["n"], d["time"], d["accuracy"]) for d in data["dp_bu"]]

            bb = [DataPoint(d["n"], d["time"], d["accuracy"]) for d in data["bb"]]

            greedy_r = [DataPoint(d["n"], d["time"], d["accuracy"]) for d in data["greedy_r"]]
            greedy_s = [DataPoint(d["n"], d["time"], d["accuracy"]) for d in data["greedy_s"]]
            greedy_v = [DataPoint(d["n"], d["time"], d["accuracy"]) for d in data["greedy_v"]]
            greedy_w = [DataPoint(d["n"], d["time"], d["accuracy"]) for d in data["greedy_w"]]

            sa = [DataPoint(d["n"], d["time"], d["accuracy"]) for d in data["sa"]]


            plt.figure(fig_nr)
            plt.title(f"capacity: {c} - scenario: {s},  space - time")

            plt.plot([dp.n for dp in dp_td], [dp.time for dp in dp_td], "or", label="top down dp")
            plt.plot([dp.n for dp in dp_bu], [dp.time for dp in dp_bu], "og", label="bottom up dp")
            plt.plot([dp.n for dp in bb], [dp.time for dp in bb], "ob", label="branch and bound")
            plt.plot([dp.n for dp in greedy_r], [dp.time for dp in greedy_r], "oy", label="greedy - ratio")
            plt.plot([dp.n for dp in greedy_s], [dp.time for dp in greedy_s], "oc", label="greedy - stats")
            plt.plot([dp.n for dp in greedy_v], [dp.time for dp in greedy_v], "om", label="greedy - value")
            plt.plot([dp.n for dp in greedy_w], [dp.time for dp in greedy_w], "ok", label="greedy - weight") # :)
            plt.plot([dp.n for dp in sa], [dp.time for dp in sa], "o", color="purple", label="simulated annealing")

            plt.plot([dp.n for dp in dp_td], [dp.time for dp in dp_td], "r")
            plt.plot([dp.n for dp in dp_bu], [dp.time for dp in dp_bu], "g")
            plt.plot([dp.n for dp in bb], [dp.time for dp in bb], "b")
            plt.plot([dp.n for dp in greedy_r], [dp.time for dp in greedy_r], "y")
            plt.plot([dp.n for dp in greedy_s], [dp.time for dp in greedy_s], "c")
            plt.plot([dp.n for dp in greedy_v], [dp.time for dp in greedy_v], "m")
            plt.plot([dp.n for dp in greedy_w], [dp.time for dp in greedy_w], "k")
            plt.plot([dp.n for dp in sa], [dp.time for dp in sa], color="purple")

            plt.xlabel("n")
            plt.ylabel("time")

            plt.legend()
            plt.show()

            plt.figure(fig_nr + 1)
            plt.title(f"capacity: {c} - scenario: {s}, space - accuracy")

            # create a box plot
            data = {
                "greedy ratio": [dp.accuracy for dp in greedy_r],
                "greedy stats": [dp.accuracy for dp in greedy_s],
                "greedy value": [dp.accuracy for dp in greedy_v],
                "greedy weight": [dp.accuracy for dp in greedy_w],
                "simulated anneling": [dp.accuracy for dp in sa]
            }
            df = pd.DataFrame(data)

            accuracy_data = df[["greedy ratio", "greedy stats", "greedy value", "greedy weight", "simulated anneling"]].melt()
            
            sns.boxplot(x='variable', y='value', data=accuracy_data)
            plt.xticks(rotation=45)
            plt.xlabel("algorithm")
            plt.ylabel("accuracy")
            plt.title(f"capacity: {c} - scenario: {s}, space - accuracy")

            plt.xlabel("n")
            plt.ylabel("accuracy")

            plt.legend()
            plt.show()

            plt.figure(fig_nr + 2)
            plt.title(f"capacity: {c} - scenario: {s}, time - accuracy")

            plt.plot([dp.time for dp in greedy_r], [dp.accuracy for dp in greedy_r], "oy", label="greedy by ratio")
            plt.plot([dp.time for dp in greedy_s], [dp.accuracy for dp in greedy_s], "oc", label="greedy by stats")
            plt.plot([dp.time for dp in greedy_v], [dp.accuracy for dp in greedy_v], "om", label="greedy by value")
            plt.plot([dp.time for dp in greedy_w], [dp.accuracy for dp in greedy_w], "ok", label="greedy by weight")
            plt.plot([dp.time for dp in sa], [dp.accuracy for dp in sa], "o", color="purple", label="simulated annealing")

            plt.xlabel("time")
            plt.ylabel("accuracy")

            plt.legend()
            plt.show()

            plt.figure(fig_nr + 3)
            plt.title(f"capacity: {c} - scenario: {s}, efficiency")
            
            plt.plot([dp.n for dp in dp_td], [dp.accuracy / dp.time for dp in dp_td], label="top down dp")
            plt.plot([dp.n for dp in dp_bu], [dp.accuracy / dp.time for dp in dp_bu], label="bottom up dp")
            plt.plot([dp.n for dp in bb], [dp.accuracy / dp.time for dp in bb], label="branch and bound")
            plt.plot([dp.n for dp in greedy_r], [dp.accuracy / dp.time for dp in greedy_r], label="greedy by ratio")
            plt.plot([dp.n for dp in greedy_s], [dp.accuracy / dp.time for dp in greedy_s], label="greedy by stats")
            plt.plot([dp.n for dp in greedy_v], [dp.accuracy / dp.time for dp in greedy_v], label="greedy by value")
            plt.plot([dp.n for dp in greedy_w], [dp.accuracy / dp.time for dp in greedy_w], label="greedy by weight")
            plt.plot([dp.n for dp in sa], [dp.accuracy / dp.time for dp in sa], label="simulated annealing")

            plt.xlabel("n")
            plt.ylabel("efficiency")

            plt.legend()

            fig_nr += 4


if __name__ == '__main__':
    do_analysis()
