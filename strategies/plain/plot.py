import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import re
from collections import defaultdict
import numpy as np
from scipy.ndimage import gaussian_filter1d

# Read data from file
filename = 'm1n6.dat'
with open(filename, 'r') as f:
    lines = f.readlines()

# Data structure: data[metric_index][config_name][U] = list of values
data = [defaultdict(lambda: defaultdict(list)) for _ in range(4)]

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
    'Anterior Security',
    'Posterior Security',
    'Pincer Security',
    'Schedule Entropy',
]

marker_map = {
    'TS0PB0BU0RP0': '',
    'TS0PB0BU0RP1': 's',

    'TS1PB0BU0RP0': '',
    'TS1PB0BU1RP0': '^',

    'TS1PB0BU0RP1': 'o',
    'TS1PB0BU1RP1': 'x',

    'TS1PB1BU0RP0': 's',
    'TS1PB1BU1RP0': '^',

    'TS1PB1BU0RP1': '^',
    'TS1PB1BU1RP1': 'x',
}

color_map = {
    'TS0PB0BU0RP0': 'grey',
    'TS0PB0BU0RP1': 'black',

    'TS1PB0BU0RP0': 'black',
    'TS1PB0BU1RP0': 'blue',

    'TS1PB0BU0RP1': 'green',
    'TS1PB0BU1RP1': 'red',

    'TS1PB1BU0RP0': 'red',
    'TS1PB1BU1RP0': 'blue',

    'TS1PB1BU0RP1': 'blue',
    'TS1PB1BU1RP1': 'red',
}

style_map = {
    'TS0PB0BU0RP0': '--',
    'TS0PB0BU0RP1': '-',

    'TS1PB0BU0RP0': ':',
    'TS1PB0BU1RP0': '-',

    'TS1PB0BU0RP1': '-',
    'TS1PB0BU1RP1': '-',

    'TS1PB1BU0RP0': '-',
    'TS1PB1BU1RP0': '-',

    'TS1PB1BU0RP1': '-',
    'TS1PB1BU1RP1': '-',
}

def label_maker(config_name):
    label = []

    if 'TS0' in config_name and 'RP0' in config_name:
        label.append('RM')
    
    if 'TS0' in config_name and 'RP1' in config_name:
        label.append('FixPri')

    if 'RP1' in config_name:
        label.append('RePri')

    if 'PB1' in config_name:
        if len(label) > 0:
            label.append('PushB.')
        else:
            label.append('PushBack')
    
    if 'BU1' in config_name:
        if len(label) > 0:
            label.append('Bud.')
        else:
            label.append('Budget')

    if len(label) == 0:
        return 'TaskShuffler'
    
    return ' + '.join(label)
    

for i, metric_data in enumerate(data):
    plt.figure(dpi=1200, figsize=(11, 6))
    legend_handles = []
    for config_name in sorted(metric_data.keys()):

        """if config_name not in ['TS0PB0BU0RP0', 'TS1PB0BU0RP0',
                                'TS1PB1BU0RP0',
                                'TS1PB1BU0RP1',
                                'TS1PB0BU0RP1',
                                'TS1PB1BU1RP1']:
            continue"""
        
        if config_name not in ['TS1PB0BU0RP0', 'TS1PB1BU0RP0']:
            continue

        u_vals = sorted(metric_data[config_name].keys())
        y_means = [np.mean(metric_data[config_name][u]) for u in u_vals]

        if len(u_vals) < 2:
            continue  # not enough data to plot

        # Apply smoothing
        y_smoothed = gaussian_filter1d(y_means, sigma=3.0)

        marker = marker_map[config_name]  # store for legend
        color = color_map[config_name]
        line_style = style_map[config_name]

        plt.plot(u_vals, y_smoothed, marker+line_style, color=color, label=config_name, markersize=8, markevery=0.1, linewidth=2)

        # Create a custom legend entry
        legend_handles.append(Line2D(
            [0], [0],
            color=color,
            marker=marker,
            linestyle=line_style,
            label='ON' if 'PB1' in config_name else 'OFF',
            #label=label_maker(config_name),
            markersize=6,
            linewidth=2,
        ))

    plt.title(f'{metric_names[i]} (m=1, n=6, f=1)', fontsize=18)
    plt.xlabel('Utilization (U)', fontsize=16)
    plt.xticks(fontsize=14)
    plt.ylabel(f'Average {metric_names[i]}', fontsize=16)
    plt.yticks(fontsize=14)
    plt.legend(handles=legend_handles, title='Pushback', fontsize=14, title_fontsize=16, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.tight_layout()
    plt.xlim(-0.05, 0.95)
    if i < 3:
        plt.ylim(0, 1)
    else:
        plt.ylim(0, 6000)
    
    plt.savefig(f"Pushback{i}.png")

#plt.show()
