import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import re
from collections import defaultdict
import numpy as np
from scipy.ndimage import gaussian_filter1d

# Read data from file
filename = 'm4n25f1_2.dat'
with open(filename, 'r') as f:
    lines = f.readlines()

# Data structure: data[metric_index][config_name][U] = list of values
data = [defaultdict(lambda: defaultdict(list)) for _ in range(8)]

# Regex to extract U and configs like Plain=(...), TS+Push=(...), etc.
# Matches: AnyWord=(v1,v2,v3,v4,)
config_pattern = re.compile(r'([A-Za-z0-9_+\-]+)=\(([\d.,]+)\)')

color_map = {
    'IU': 'blue',
    'DU': 'red',
    'RM': 'green'
}

marker_map = {
    'BF': 'o',
    'WF': 's',
    'FF': '^',
}

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
    fig = plt.figure(dpi=1200, figsize=(10, 6))
    legend_handles = []
    for config_name in sorted(metric_data.keys()):

        #if config_name not in ['WF-IU', 'WF-RM', 'WF-DU']: # 'WF-minm2', 'WF-minm3']:
        if 'WF' in config_name:
            continue

        if '50' in config_name:
            continue
        
        u_vals = sorted(metric_data[config_name].keys())
        y_means = [np.mean(metric_data[config_name][u]) for u in u_vals]

        if len(u_vals) < 2:
            continue  # not enough data to plot

        # Apply smoothing
        y_smoothed = gaussian_filter1d(y_means, sigma=3.0)

        color = 'black'
        line_style = '-' if 'BF' in config_name else '--'

        if 'IU' in config_name:
            color = color_map['IU']
            marker = marker_map['BF']

        elif 'DU' in config_name:
            color = color_map['DU']
            marker = marker_map['WF']

        elif 'RM' in config_name:
            color = color_map['RM']
            marker = marker_map['FF']


        """marker = ''
        if 'BF' in config_name:
            marker = marker_map['BF']
        elif 'WF' in config_name:
            marker = marker_map['WF']
        elif 'FF' in config_name:
            marker = marker_map['FF']
        """
        
        if 'minm' in config_name:
            marker = 'x'

        if '2' in config_name:
            line_style = '--'
        
        if '3' in config_name:
            line_style = '-.'
            marker = ''

        plt.plot(u_vals, y_smoothed, marker+line_style, color=color, label=config_name, markersize=8, markevery=0.1, linewidth=2)
        # Overlay sparse markers at U = 0.05 * k
        u_marker_positions = [u for u in u_vals if abs((u * 100) % 20) < 1e-6]  # i.e., u = 0.05 * k

        # Create a custom legend entry
        legend_handles.append(Line2D(
            [0], [0],
            color=color,
            marker=marker,
            linestyle=line_style,
            #label='ON' if 'BU1' in config_name else 'OFF',
            label=config_name,
            markersize=6
        ))

    plt.title(f'{metric_names[i]} (m=4, n=25, f=1)', fontsize=18)
    plt.xlabel('Utilization (U)', fontsize=16)
    plt.xticks(fontsize=14)
    plt.ylabel(f'Average {metric_names[i]}', fontsize=16)
    plt.yticks(fontsize=14)
    plt.legend(handles=legend_handles, title='Algorithm', fontsize=14, title_fontsize=16, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    if i < 6:
        plt.ylim(0, 1)
    
    plt.tight_layout()  # Adjust layout to make room for legend
    #plt.show()

    plt.savefig(f'FFBF_{i}.png')