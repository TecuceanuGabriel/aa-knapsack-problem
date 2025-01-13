from tests.generate_tests import test_sizes, scenarios, capacities

from src.data_point import DataPoint

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import seaborn as sns

import json
import os
import math

matplotlib.use('Qt5Agg')
plt.rcParams['figure.figsize'] = [12, 8]
# print(plt.style.available)
plt.style.use('seaborn-v0_8-notebook')


def normalize_data(data, method='standard'):
    if not data:
        return data
        
    data = np.array(data)

    if method == 'minmax':
        min_val = np.min(data)
        max_val = np.max(data)
        if max_val == min_val:
            return [1.0] * len(data)
        return (data - min_val) / (max_val - min_val)

    elif method == 'standard':
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return [0.0] * len(data)
        return (data - mean) / std

    elif method == 'log':
        min_positive = np.min(data[data > 0]) if any(data > 0) else 1
        return np.log1p(data + min_positive * 0.01)

    elif method == 'percent':
        max_val = np.max(data)
        if max_val == 0:
            return [0.0] * len(data)
        return (data / max_val) * 100
    return data


def convert_to_datapoints(data_list):
    return [DataPoint(d["n"], d["capacity"], d["time"], d["accuracy"]) 
            for d in data_list]


def write_results_to_report(f, capacity, scenario, algorithm_results, fig_nr):
    """Write algorithm comparison results as three LaTeX tables."""
    eps = 1e-8
    f.write(f"% Results for capacity: {capacity} - scenario: {scenario} (figures {fig_nr} - {fig_nr + 2})\n\n")
    
    algorithms = list(algorithm_results.keys())
    exact_methods = ['dp_td', 'dp_bu', 'bb']
    approx_methods = ['greedy_r', 'greedy_s', 'greedy_v', 'greedy_w', 'sa']
    
    problem_sizes = [(result.n, result.capacity) 
                    for result in algorithm_results[algorithms[0]]]
    
    # Exact Methods Time Table
    f.write("\\begin{table}[H]\n")
    f.write("\\centering\n")
    f.write("\\caption{Execution Time Comparison (Exact Methods) - " + 
            f"Capacity: {capacity}, Scenario: {scenario}" + 
            "}\n")
    f.write("\\label{tab:time_exact_" + f"cap{capacity}_" + 
            f"{scenario}" + "}\n")
    
    f.write("\\begin{tabular}{|l|" + "c|" * len(exact_methods) + "}\n")
    f.write("\\hline\n")
    
    f.write("n & ")
    exact_names = [algo.replace('_', ' ').upper() for algo in exact_methods]
    f.write(" & ".join(exact_names) + " \\\\\n")
    f.write("\\hline\n")
    
    # Find best times for each problem size (exact methods)
    best_times_exact = []
    for i in range(len(problem_sizes)):
        times = [algorithm_results[algo][i].time for algo in exact_methods]
        best_times_exact.append(min(times))
    
    for i, size in enumerate(problem_sizes):
        row = [f"{size[0]}"]
        for algo in exact_methods:
            result = algorithm_results[algo][i]
            if abs(result.time - best_times_exact[i]) < eps:
                row.append(f"\\textbf{{{result.time:.6f}s}}")
            else:
                row.append(f"{result.time:.6f}" + "s" if result.time != math.inf else "inf")
        f.write(" & ".join(row) + " \\\\\n")
    
    f.write("\\hline\n")
    f.write("\\end{tabular}\n")
    f.write("\\end{table}\n\n")
    
    # Approximate Methods Time Table
    f.write("\\begin{table}[H]\n")
    f.write("\\centering\n")
    f.write("\\caption{Execution Time Comparison (Approximate Methods) - " + 
            f"Capacity: {capacity}, Scenario: {scenario}" + 
            "}\n")
    f.write("\\label{tab:time_approx_" + f"cap{capacity}_" + 
            f"{scenario}" + "}\n")
    
    f.write("\\begin{tabular}{|l|" + "c|" * len(approx_methods) + "}\n")
    f.write("\\hline\n")
    
    f.write("n & ")
    approx_names = [algo.replace('_', ' ').upper() for algo in approx_methods]
    f.write(" & ".join(approx_names) + " \\\\\n")
    f.write("\\hline\n")
    
    # Find best times for each problem size (approximate methods)
    best_times_approx = []
    for i in range(len(problem_sizes)):
        times = [algorithm_results[algo][i].time for algo in approx_methods]
        best_times_approx.append(min(times))
    
    for i, size in enumerate(problem_sizes):
        row = [f"{size[0]}"]
        for algo in approx_methods:
            result = algorithm_results[algo][i]
            if abs(result.time - best_times_approx[i]) < eps:
                row.append(f"\\textbf{{{result.time:.6f}s}}")
            else:
                row.append(f"{result.time:.6f}s")
        f.write(" & ".join(row) + " \\\\\n")
    
    f.write("\\hline\n")
    f.write("\\end{tabular}\n")
    f.write("\\end{table}\n\n")
    
    # Accuracy Table (only for approximate methods)
    f.write("\\begin{table}[H]\n")
    f.write("\\centering\n")
    f.write("\\caption{Solution Quality Comparison - " + 
            f"Capacity: {capacity}, Scenario: {scenario}" + 
            "}\n")
    f.write("\\label{tab:accuracy_" + f"cap{capacity}_" + 
            f"{scenario}" + "}\n")
    
    f.write("\\begin{tabular}{|l|" + "c|" * len(approx_methods) + "}\n")
    f.write("\\hline\n")
    
    f.write("n & ")
    f.write(" & ".join(approx_names) + " \\\\\n")
    f.write("\\hline\n")
    
    # Find best accuracies for each problem size
    best_accuracies = []
    for i in range(len(problem_sizes)):
        accuracies = [algorithm_results[algo][i].accuracy for algo in approx_methods]
        best_accuracies.append(max(accuracies))
    
    for i, size in enumerate(problem_sizes):
        row = [f"{size[0]}"]
        for algo in approx_methods:
            result = algorithm_results[algo][i]
            if abs(result.accuracy - best_accuracies[i]) < eps:
                row.append(f"\\textbf{{{result.accuracy:.2f}\\%}}")
            else:
                row.append(f"{result.accuracy:.2f}\\%")
        f.write(" & ".join(row) + " \\\\\n")
    
    f.write("\\hline\n")
    f.write("\\end{tabular}\n")
    f.write("\\end{table}\n\n")


def plot_time_comparison(algorithm_results, capacity, scenario, fig_nr):
    plt.figure(fig_nr)

    # plt.title(f"Capacity: {capacity} - Scenario: {scenario}\nTime Comparison (Log Normalized)")

    colors = {'dp_td': 'r', 'dp_bu': 'g', 'bb': 'b', 'greedy_r': 'y',
             'greedy_s': 'c', 'greedy_v': 'm', 'greedy_w': 'k', 'sa': 'purple'}
    labels = {
        'dp_td': 'top down dp', 'dp_bu': 'bottom up dp', 
        'bb': 'branch and bound', 'greedy_r': 'greedy - ratio',
        'greedy_s': 'greedy - stats', 'greedy_v': 'greedy - value',
        'greedy_w': 'greedy - weight', 'sa': 'simulated annealing'
    }

    all_times = []
    for data in algorithm_results.values():
        all_times.extend([dp.time for dp in data])
    
    normalized_times = normalize_data(all_times, 'log')
    time_dict = dict(zip(all_times, normalized_times))

    for algo, data in algorithm_results.items():
        color = colors[algo]
        x_vals = [dp.n for dp in data]
        y_vals = [time_dict[dp.time] for dp in data]
        
        plt.scatter(x_vals, y_vals, c=color, label=labels[algo], alpha=0.7, s=100)
        plt.plot(x_vals, y_vals, color, alpha=0.5, linewidth=2)

    plt.xlabel("n (problem size)")
    plt.ylabel("Normalized Time (s)")
    plt.grid(True, alpha=0.3)
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"tests/out/plots/{fig_nr}_{capacity}_{scenario}_time_comparison.svg", format='svg', bbox_inches='tight', dpi=1200)

    plt.show()


def plot_accuracy_comparison(algorithm_results, capacity, scenario, fig_nr):
    plt.figure(fig_nr + 1)

    # plt.title(f"Capacity: {capacity} - Scenario: {scenario}\nAccuracy Comparison (Percent)")

    accuracy_data = {}
    for algo_name in ['greedy_r', 'greedy_s', 'greedy_v', 'greedy_w', 'sa']:
        accuracies = [dp.accuracy for dp in algorithm_results[algo_name]]
        normalized_accuracies = normalize_data(accuracies, 'percent')
        accuracy_data[algo_name.replace('_', ' ')] = normalized_accuracies

    df = pd.DataFrame(accuracy_data)
    accuracy_melted = df.melt()
    
    sns.boxplot(x='variable', y='value', data=accuracy_melted)
    plt.xticks(rotation=45)
    plt.xlabel("Algorithm")
    plt.ylabel("Normalized Accuracy (%)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(f"tests/out/plots/{fig_nr + 1}_{capacity}_{scenario}_accuracy_comparison.svg", format='svg', bbox_inches='tight', dpi=1200)

    plt.show()


def plot_efficiency_comparison(algorithm_results, capacity, scenario, fig_nr):
    plt.figure(fig_nr + 2)

    # plt.title(f"Capacity: {capacity} - Scenario: {scenario}\nEfficiency Comparison (MinMax)")

    all_efficiencies = []
    for data in algorithm_results.values():
        all_efficiencies.extend([dp.accuracy / dp.time for dp in data])
        
    normalized_efficiencies = normalize_data(all_efficiencies, 'log')
    efficiency_dict = dict(zip(all_efficiencies, normalized_efficiencies))

    for algo, data in algorithm_results.items():
        x_vals = [dp.n for dp in data]
        efficiencies = [dp.accuracy / dp.time for dp in data]
        y_vals = [efficiency_dict[eff] for eff in efficiencies]
        
        plt.plot(x_vals, y_vals, 'o-', label=algo.replace('_', ' '), 
                linewidth=2, markersize=8, alpha=0.7)

    plt.xlabel("n (problem size)")
    plt.ylabel("Normalized Efficiency (accuracy / time = % / s)")
    plt.grid(True, alpha=0.3)
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"tests/out/plots/{fig_nr + 2}_{capacity}_{scenario}_efficiency_comparison.svg", format='svg', bbox_inches='tight', dpi=1200)

    plt.show()

def load_data(data_path):
    """Load test results from JSON file."""
    with open(data_path, "r") as f:
        return json.load(f)

def analyze_algorithms(data_path = "tests/out/data.json", report_path = "tests/out/report.txt"):
    """Perform complete analysis of all test scenarios and capacities."""
    data = load_data(data_path)
    fig_nr = 0
    
    with open(report_path, "w") as f:
        for capacity in capacities:
            str_capacity = str(capacity)
            for scenario in scenarios:
                algorithm_results = {
                    algo: convert_to_datapoints(data[str_capacity][scenario][algo])
                    for algo in ['dp_td', 'dp_bu', 'bb', 'greedy_r', 'greedy_s', 
                               'greedy_v', 'greedy_w', 'sa']
                }

                write_results_to_report(f, str_capacity, scenario, algorithm_results, fig_nr)
                plot_time_comparison(algorithm_results, str_capacity, scenario, fig_nr)
                plot_accuracy_comparison(algorithm_results, str_capacity, scenario, fig_nr)
                plot_efficiency_comparison(algorithm_results, str_capacity, scenario, fig_nr)
                
                fig_nr += 3

if __name__ == '__main__':
    os.makedirs("tests/out/plots", exist_ok=True)
    analyze_algorithms()
