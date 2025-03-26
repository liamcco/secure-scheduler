import numpy as np
import matplotlib.pyplot as plt
import re
from collections import defaultdict

# Step 1: Read and parse the file
file_path = "ant1.txt"
ant_data = defaultdict(list)

with open(file_path, "r") as file:
    for line in file:
        match = re.match(r"n=(\d+),ANT=([\d.]+)", line.strip())
        if match:
            n = int(match.group(1))  # Extract integer n
            ant = float(match.group(2))  # Extract float ANT
            ant_data[n].append(ant)

# Step 2: Compute the average ANT for each n
n_values = sorted(ant_data.keys())  # Get sorted unique n values
avg_ant_values = [np.mean(ant_data[n]) for n in n_values]  # Compute averages

# Step 3: Plot the results
plt.figure(figsize=(10, 6))
plt.plot(n_values, avg_ant_values, marker='o', linestyle='-', color='b')

plt.xlabel("n")
plt.ylabel("Average ANT")
plt.title("Average ANT as a Function of n")
plt.grid(True)
plt.xlim(min(n_values) - 1, max(n_values) + 1)
plt.ylim(0, 1.03)

plt.show()
