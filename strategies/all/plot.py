import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import re
from collections import defaultdict
import numpy as np
from scipy.ndimage import gaussian_filter1d

# Read data from file
filename = 'm4n25f3wfdu.dat'
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

marker_map = {
    'RP0MI0PB0BU0': '',
    'RP0MI0PB0BU1': 'o',
    'RP0MI0PB1BU0': '',
    'RP0MI0PB1BU1': '^',
    'RP0MI1PB0BU0': '',
    'RP0MI1PB0BU1': 'o',
    'RP0MI1PB1BU0': '',
    'RP0MI1PB1BU1': '^',
    'RP1MI0PB0BU0': '',
    'RP1MI0PB0BU1': 's',
    'RP1MI0PB1BU0': '',
    'RP1MI0PB1BU1': 'x',
    'RP1MI1PB0BU0': '',
    'RP1MI1PB0BU1': 's',
    'RP1MI1PB1BU0': '',
    'RP1MI1PB1BU1': 'x',
}

color_map = {
    'RP0MI0PB0BU0': 'black',
    'RP0MI0PB0BU1': 'blue',
    'RP0MI0PB1BU0': 'b',
    'RP0MI0PB1BU1': 'red',
    'RP0MI1PB0BU0': 'b',
    'RP0MI1PB0BU1': 'blue',
    'RP0MI1PB1BU0': 'b',
    'RP0MI1PB1BU1': 'red',
    'RP1MI0PB0BU0': 'r',
    'RP1MI0PB0BU1': 'green',
    'RP1MI0PB1BU0': 'r',
    'RP1MI0PB1BU1': 'black',
    'RP1MI1PB0BU0': 'r',
    'RP1MI1PB0BU1': 'green',
    'RP1MI1PB1BU0': 'r',
    'RP1MI1PB1BU1': 'black',
}

style_map = {
    'RP0MI0PB0BU0': '-',
    'RP0MI0PB0BU1': '-',
    'RP0MI0PB1BU0': '-',
    'RP0MI0PB1BU1': '-',
    'RP0MI1PB0BU0': '--',
    'RP0MI1PB0BU1': '--',
    'RP0MI1PB1BU0': '--',
    'RP0MI1PB1BU1': '--',
    'RP1MI0PB0BU0': '-',
    'RP1MI0PB0BU1': '-',
    'RP1MI0PB1BU0': '-',
    'RP1MI0PB1BU1': '-',
    'RP1MI1PB0BU0': '--',
    'RP1MI1PB0BU1': '--',
    'RP1MI1PB1BU0': '--',
    'RP1MI1PB1BU1': '--',
}

width_map = {
    'RP0MI0PB0BU0': '2',
    'RP0MI0PB0BU1': '2',
    'RP0MI0PB1BU0': '2',
    'RP0MI0PB1BU1': '1',
    'RP0MI1PB0BU0': '2',
    'RP0MI1PB0BU1': '1',
    'RP0MI1PB1BU0': '2',
    'RP0MI1PB1BU1': '1',
    'RP1MI0PB0BU0': '2',
    'RP1MI0PB0BU1': '1',
    'RP1MI0PB1BU0': '2',
    'RP1MI0PB1BU1': '1',
    'RP1MI1PB0BU0': '2',
    'RP1MI1PB0BU1': '1',
    'RP1MI1PB1BU0': '2',
    'RP1MI1PB1BU1': '1',
}

def label_maker(config_name):
    label = []

    if 'RP1' in config_name:
        label.append('RePri')

    if 'PB1' in config_name:
        label.append('PushB.')

    if 'MI1' in config_name:
        label.append('Migr.')

    #if 'BU1' in config_name:
    #    label.append('Budget')
    
    if len(label) == 0:
        return 'TaskShuffler + Budget'

    return ' + '.join(label)

for i, metric_data in enumerate(data):
    plt.figure(dpi=1200, figsize=(10, 6))
    legend_handles = []
    for config_name in sorted(metric_data.keys()):

        #filter!!
        if 'BU0' in config_name:
            continue

        #filter!!
        if config_name not in ['RP0MI0PB0BU0', 'RP0MI0PB0BU1']:
            pass
        
        u_vals = sorted(metric_data[config_name].keys())
        y_means = [np.mean(metric_data[config_name][u]) for u in u_vals]

        if len(u_vals) < 2:
            continue  # not enough data to plot

        # Apply smoothing
        y_smoothed = gaussian_filter1d(y_means, sigma=3.0)

        marker = marker_map[config_name]  # store for legend
        color = color_map[config_name]
        line_style = style_map[config_name]
        line_width = 2 #width_map[config_name]

        plt.plot(u_vals, y_smoothed, marker+line_style, color=color, label=config_name, linewidth=line_width, markersize=8, markevery=0.1)

        # Create a custom legend entry
        legend_handles.append(Line2D(
            [0], [0],
            color=color,
            marker=marker,
            linestyle=line_style,
            #label='ON' if 'BU1' in config_name else 'OFF',
            label=label_maker(config_name),
            markersize=6
        ))

    plt.title(f'{metric_names[i]} (m=4, n=25, f=1)', fontsize=18)
    plt.xlabel('Utilization (U)', fontsize=16)
    plt.xticks(fontsize=14)
    plt.ylabel(f'Average {metric_names[i]}', fontsize=16)
    plt.yticks(fontsize=14)
    plt.xlim(-0.05, 3.4)
    plt.legend(handles=legend_handles, title='Configuration', fontsize=14, title_fontsize=16, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.tight_layout()
    if i < 6:
        plt.ylim(0, 1)
    else:
        plt.ylim(0, 10000)

    plt.savefig(f'ALLf3_{i}.png')

#plt.show()