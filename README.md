https://github.com/TecuceanuGabriel/aa-knapsack-problem

# Installation

To install the required packages run:

```bash
pip install -r requirements.txt
```

To generate and run the tests run:

```bash
python run_all.py
```

To get the plots run:

```bash
python analyze_data.py
```

# File Structure

- `run_all.py`: generates and runs the tests
- `analyze_data.py`: analyzes the data and generates the plots
- tests:
  - in: contains the input files for each test
  - out:
    - output directories for each algorithm
    - plot: contains the generated plots
    - data.json: the result of run_all.py
    - report.txt: result of each scenario formated as latex table
    - profile.txt: profiling results

# Tests

For our measurements to be accurate we generate the test cases in the following way:

1. have various problem sizes:

```python
test_sizes = [20, 100, 250, 500, 750, 1000, 3000, 5000, 8000, 10000]
```

2. have various capacities:

```python
capacities = ['low', 'medium', 'high']
```

3. have various value/wieght distributions:

```python
distributions = ['random', 'uniform', 'high value/weight ratio', 'low value/weight ratio']
```

We generate a test for each combination, resultin 120 test cases.

# Measurements

To measure time we use the timeit module, which runs each test NR_RUNS (=10) times and returns the total time, we then divide by NR_RUNS to get the average time.

# Plotting

For plotting we use the matplotlib, pandas, numpy and seaborn libraries.

For each scenario (capacity - distribution combination) we plot:

- the Problem Size vs Average Time for each algorithm
- the Accuracy variation as a box and whisker plot for the approximation algorithms
- the Efficiency (accuracy/time) vs Problem Size for each algorithm
