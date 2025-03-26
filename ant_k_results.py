import numpy as np
import matplotlib.pyplot as plt

# Load the data
file_path = 'ant_k.opadu.txt'  # Pretend this file exists
data = []
with open(file_path, 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split(',')
        k = int(parts[0].split('=')[1])
        U = float(parts[1].split('=')[1])
        ANT = float(parts[2].split('=')[1])
        POST = float(parts[3].split('=')[1])
        PINCH = float(parts[4].split('=')[1])
        if (U < 0.8):
            data.append((k, U, ANT, POST, PINCH))

# Define utilization groups (bins)
U_bins = np.linspace(0, 1, 7)  # 5 bins (e.g., [0, 0.2), [0.2, 0.4), etc.)
U_labels = [(U_bins[i], U_bins[i+1]) for i in range(len(U_bins)-1)]

# Organize data into bins and compute averages
def compute_avg(metric_index):
    avg_metric = {}
    for entry in data:
        k, U, *metrics = entry
        metric_value = metrics[metric_index]
        for U_min, U_max in U_labels:
            if U_min <= U < U_max:
                key = (k, (U_min, U_max))
                if key not in avg_metric:
                    avg_metric[key] = []
                avg_metric[key].append(metric_value)
    
    for key in avg_metric:
        avg_metric[key] = sum(avg_metric[key]) / len(avg_metric[key])
    
    return avg_metric

metrics = {"ANT": 0, "POST": 1, "PINCH": 2}

for metric_name, index in metrics.items():
    avg_metric = compute_avg(index)
    
    # Prepare data for plotting
    U_group_names = [f'[{U_min:.1f}, {U_max:.1f})' for U_min, U_max in U_labels]
    plot_data = {group: ([], []) for group in U_group_names}  # k values and metric values

    for (k, (U_min, U_max)), value in avg_metric.items():
        group_name = f'[{U_min:.1f}, {U_max:.1f})'
        plot_data[group_name][0].append(k)
        plot_data[group_name][1].append(value)
    
    # Plot
    plt.figure(figsize=(10, 6))
    for group_name, (k_vals, metric_vals) in plot_data.items():
        if not k_vals:
            continue  # Skip empty groups
        
        # Sort k values and corresponding metric values
        sorted_k_vals, sorted_metric_vals = zip(*sorted(zip(k_vals, metric_vals)))
        
        plt.plot(sorted_k_vals, sorted_metric_vals, marker='o', label=group_name)

    plt.xlabel('k (Compromised Tasks)')
    plt.ylabel(f'Average {metric_name}')
    plt.title(f'Effect of k on {metric_name} for Different U Groups')
    plt.legend(title='U Groups')
    plt.grid(True)
    plt.ylim(0, 1.03)

plt.show()
