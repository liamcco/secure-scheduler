import numpy as np
import matplotlib.pyplot as plt
import re
from collections import defaultdict
from scipy.ndimage import gaussian_filter1d

# Step 1: Read file and parse data
file_path = "lackmusCPTEST.txt"
data = defaultdict(list)

with open(file_path, "r") as file:
    for line in file:
        match = re.match(r"U=([\d.]+):(.+)", line.strip())
        if match:
            U = float(match.group(1))
            points = re.findall(r"\(([\d.]+),([\d.]+)\)", match.group(2))
            points = [(float(f), float(E)) for f, E in points]
            data[U] = points

# Step 2: Bin U-values into 0.05 groups
bin_size = 0.1
binned_data = defaultdict(lambda: defaultdict(list))

for U, points in data.items():
    U_bin = round(np.floor(U / bin_size) * bin_size, 2)  # Assign U to a bin
    for f, E in points:
        binned_data[U_bin][f].append(E)

# Step 3: Compute averages
averaged_data = {U_bin: {} for U_bin in binned_data}
for U_bin, f_values in binned_data.items():
    for f, E_list in f_values.items():
        averaged_data[U_bin][f] = np.mean(E_list)

# Step 4: Plot the smoothened curves
plt.figure(figsize=(10, 6))
for U_bin, f_values in sorted(averaged_data.items()):
    if U_bin > 0.5:  # Skip U-values greater than 0.6
        pass
    f_sorted = sorted(f_values.keys())
    E_avg = np.array([averaged_data[U_bin][f] for f in f_sorted])

    # Apply Gaussian smoothing
    E_smooth = gaussian_filter1d(E_avg, sigma=2)

    plt.plot(f_sorted, E_smooth, label=f"U_bin={U_bin:.2f}")

plt.xlabel("f")
plt.ylabel("E (Smoothed Average)")
plt.title("Smoothed Effect of f on E for Binned U-values")
plt.legend()
plt.grid()
plt.show()
