import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.ndimage import gaussian_filter1d

# === USER INPUT ===
filename = "m1n6.dat"
#metrics_to_plot = ["FF-RM","FF-DU","FF-IU", "Min", "Avg"]  # Customize this list
#metrics_to_plot = ["WF-RM","WF-DU","WF-IU", "Min", "Avg"]  # Customize this list
#metrics_to_plot = ["BF-RM","BF-DU","BF-IU", "Min", "Avg"]  # Customize this list
#metrics_to_plot = ["WF-minm", "WF-minm2", "WF-minm3", "Min", "Avg"]  # Customize this list
metrics_to_plot = ["RM", "DU", "IU", "SM", "RSM", "Min", "Avg"]  # Customize this list

# === Parse File ===
grouped = defaultdict(lambda: defaultdict(list))  # grouped[U][metric] = list of values

with open(filename, "r") as f:
    for line in f:
        parts = line.strip().split(',')
        if not parts or not parts[0].startswith("U="):
            continue
        try:
            u = float(parts[0].split('=')[1])
            if (u > 0.8):
                continue
            for part in parts[1:]:
                if not part:
                    continue
                key, val = part.split('=')
                grouped[u][key].append(float(val))
        except ValueError:
            print(f"Skipping malformed line: {line.strip()}")

# === Aggregate (Average) by U ===
U_vals = sorted(grouped.keys())
results_h = {metric: [] for metric in metrics_to_plot}
results_v = {metric: [] for metric in metrics_to_plot}

for u in U_vals:
    for metric in metrics_to_plot:
        h_key = f"{metric}_h"
        v_key = f"{metric}_v"
        h_vals = grouped[u].get(h_key, [np.nan])
        v_vals = grouped[u].get(v_key, [np.nan])
        results_h[metric].append(np.nanmean(h_vals))
        results_v[metric].append(np.nanmean(v_vals))

# === Plot _h ===
plt.figure(dpi=1200,figsize=(10, 6))
for metric in metrics_to_plot:

    if "RM" in metric:
        marker = 'o'
    if "IU" in metric:
        marker = 's'
    if "DU" in metric:
        marker = '^'
    if "SM" in metric:
        marker = 'D'
    if "RSM" in metric:
        marker = 'x'

    smooth = gaussian_filter1d(results_h[metric], sigma=3.0)
    if (metric == "Min"):
        plt.plot(U_vals, smooth, '-', label='Min', color='grey', linewidth=2)
    elif (metric == "Avg"):
        plt.plot(U_vals, smooth, '--', label='Average', color='grey', linewidth=2)
    else:
        plt.plot(U_vals, smooth, marker+'-', label=metric, markersize=8, linewidth=2, markevery=0.1)
plt.xlabel("Utilization (U)", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel("Horizontal schedule entropy", fontsize=16)
plt.title("Horizontal Schedule Entropy vs Utilization (m=1, n=6)", fontsize=18)
plt.grid(True)
plt.legend(title='Priority', fontsize=14, title_fontsize=16, loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.ylim(0, 1.1)  # Set y-axis limit to 0-1.1 for better visibility
plt.xlim(-0.05, 0.85)  # Set x-axis limit to 0-2.4 for better visibility
max_line = plt.axhline(y=1, color="red", linestyle="--", linewidth=2, label="Max")

#plt.show()
plt.savefig("lackmusPrioritym1n6_h.png")
exit()

# === Plot _v ===
plt.figure(dpi=1200, figsize=(10, 6))
for metric in metrics_to_plot:
    if "RM" in metric:
        marker = 'o'
    if "IU" in metric:
        marker = 's'
    if "DU" in metric:
        marker = '^'
    smooth = gaussian_filter1d(results_v[metric], sigma=3.0)
    if (metric == "Min"):
        plt.plot(U_vals, smooth, '-', label='Min', color='grey', linewidth=2)
    elif (metric == "Avg"):
        plt.plot(U_vals, smooth, '--', label='Average', color='grey', linewidth=2)
    else:
        plt.plot(U_vals, smooth, marker+'-', label=metric, markersize=8, linewidth=2, markevery=0.1)
plt.xlabel("Utilization (U)", fontsize=16)
plt.xticks(fontsize=14)
plt.ylabel("Vertical schedule entropy", fontsize=16)
plt.yticks(fontsize=14)
plt.title("Vertical Schedule Entropy vs Utilization (m=1, n=6)", fontsize=18)
plt.grid(True)
plt.legend(title='Algorithm', fontsize=14, title_fontsize=16, loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.ylim(0, 1.1)  # Set y-axis limit to 0-1.1 for better visibility
plt.xlim(-0.05, 2.45)  # Set x-axis limit to 0-2.4 for better visibility
max_line = plt.axhline(y=1, color="red", linestyle="--", linewidth=2, label="Max")

#plt.show()
plt.savefig("lackmusBFm3n5_v.png")