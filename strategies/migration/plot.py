import matplotlib.pyplot as plt
import re
from collections import defaultdict
import numpy as np
from scipy.ndimage import gaussian_filter1d

# Read data from file
filename = 'm4n25wfdu.dat'
with open(filename, 'r') as f:
    lines = f.readlines()

# Data structure: data[metric_index][config_name][U] = list of values
data = [defaultdict(lambda: defaultdict(list)) for _ in range(8)]

# Regex to extract U and configs like Plain=(...), TS+Push=(...), etc.
# Matches: AnyWord=(v1,v2,v3,v4,)
config_pattern = re.compile(r'([A-Za-z0-9_+\-]+)=\(([\d.,]+)\)')

# Parse lines
for line in lines:
    u_match = re.search(r"U=([\d.]+)", line)
    if not u_match:
        continue
    u = float(u_match.group(1))

    for config_name, values in config_pattern.findall(line):
        try:
            metrics = tuple(map(float, values.strip(',').split(',')))
            for i, metric_value in enumerate(metrics):
                data[i][config_name][u].append(metric_value)
        except ValueError:
            continue  # skip malformed entries

# Plot: one figure per metric
metric_names = [
    'Hor. Anterior Security',
    'Hor. Posterior Security',
    'Hor. Pincer Security',
    'Ver. Anterior Security',
    'Ver. Posterior Security',
    'Ver. Pincer Security',
    'Hor. Schedule Entropy',
    'Ver. Schedule Entropy'
]

for i, metric_data in enumerate(data):
    plt.figure(dpi=1200, figsize=(10, 6))
    for config_name in sorted(metric_data.keys()):
        u_vals = sorted(metric_data[config_name].keys())
        y_means = [np.mean(metric_data[config_name][u]) for u in u_vals]

        if len(u_vals) < 2:
            continue  # not enough data to plot

        # Apply smoothing
        y_smoothed = gaussian_filter1d(y_means, sigma=3.0)

        # Plot smoothed line

        label = "OFF"
        if int(config_name[3:]) > 0:
            label = f"every {config_name[3:]}"

        linestyle = '-' if int(config_name[3:]) > 0 else '--'

        if int(config_name[3:]) == 0:
            marker = ''
            linestyle = '--'
        elif int(config_name[3:]) == 100:
            marker = 's'
            linestyle = '-'
        elif int(config_name[3:]) == 500:
            marker = '^'
            linestyle = '-'
        elif int(config_name[3:]) == 3000:
            marker = 'D'
            linestyle = '-'
        
        plt.plot(u_vals, y_smoothed, marker+linestyle, label=label, linewidth=2, markersize=8, markevery=0.1)

    plt.title(f'{metric_names[i]} (m=4, n=25, f=1)', fontsize=18)
    plt.xlabel('Utilization (U)', fontsize=16)
    plt.xticks(fontsize=14)
    plt.ylabel(f'Average {metric_names[i]}', fontsize=16)
    plt.yticks(fontsize=14)
    plt.legend(title='Migration', fontsize=14, title_fontsize=16, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.tight_layout()
    if i < 6:
        plt.ylim(0, 1.1)

    plt.savefig(f"migration_{i}.png")

    #plt.show()  # Show the plot for each metric

