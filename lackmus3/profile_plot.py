import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.ndimage import gaussian_filter1d

# Prepare grouped containers
grouped = defaultdict(lambda: {'Min_h': [], 'Min_v': [], 'Avg_h': [], 'Avg_v': []})

# Read and parse the file
filename = "m3n5.dat"
metrics_to_plot = ["Min", "Avg"]  # Customize this list

# === Parse File ===
grouped = defaultdict(lambda: defaultdict(list))  # grouped[U][metric] = list of values

with open(filename, "r") as f:
    for line in f:
        parts = line.strip().split(',')
        if not parts or not parts[0].startswith("U="):
            continue
        try:
            u = float(parts[0].split('=')[1])
            if (u > 2.5):
                continue
            for part in parts[1:]:
                if not part:
                    continue
                key, val = part.split('=')
                grouped[u][key].append(float(val))
        except ValueError:
            print(f"Skipping malformed line: {line.strip()}")

# Sort U values and compute averages
U_vals = sorted(grouped.keys())
Min_h_avg = [np.mean(grouped[u]['Min_h']) for u in U_vals]
Min_v_avg = [np.mean(grouped[u]['Min_v']) for u in U_vals]
Avg_h_avg = [np.mean(grouped[u]['Avg_h']) for u in U_vals]
Avg_v_avg = [np.mean(grouped[u]['Avg_v']) for u in U_vals]

# Apply smoothing
sigma = 1.0  # Standard deviation for Gaussian kernel
Min_h_smooth = gaussian_filter1d(Min_h_avg, sigma=sigma)
Min_v_smooth = gaussian_filter1d(Min_v_avg, sigma=sigma)
Avg_h_smooth = gaussian_filter1d(Avg_h_avg, sigma=sigma)
Avg_v_smooth = gaussian_filter1d(Avg_v_avg, sigma=sigma)

# Plot _h values
# For plotting one dashed horizontal line at y=1 (theoretical max)
plt.figure(figsize=(10, 5))
plt.plot(U_vals, Min_h_smooth, '-', label='Min', color='grey', linewidth=2)
plt.plot(U_vals, Avg_h_smooth, '--', label='Average', color='grey', linewidth=2)
plt.xlabel('Utilization (U)')
plt.ylabel('H Values')
plt.title(f'Horizontal schedule entropy profile for ({filename})')
plt.legend()
plt.ylim(0.0, 1.05)
plt.grid(True)
plt.tight_layout()
max_line = plt.axhline(y=1, color="red", linestyle="-", linewidth=2, label="Max")

# Plot _v values
plt.figure(figsize=(10, 5))
plt.plot(U_vals, Min_v_smooth, '-', label='Min', color='grey', linewidth=2)
plt.plot(U_vals, Avg_v_smooth, '--', label='Average', color='grey', linewidth=2)
plt.xlabel('Utilization (U)')
plt.ylabel('V Values')
plt.title(f'Vertical schedule entropy profile for ({filename})')
plt.legend()
plt.ylim(0.0, 1.05)
plt.grid(True)
plt.tight_layout()

max_line = plt.axhline(y=1, color="red", linestyle="--", linewidth=2, label="Max")
plt.show()


