import matplotlib.pyplot as plt
from collections import defaultdict

test = "CP1"

# Read and parse the data, computing averages for duplicate U-values
def parse_and_average_data(filename):
    data = defaultdict(lambda: {test: [], "Med": [], "Min": [], "Avg": []})  # Dictionary to store lists of values

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("U="):
                parts = line.split(",")
                U = float(parts[0].split("=")[1])  # Extract U value
                compd = float(parts[1].split("=")[1])  # Extract WF value
                Med = float(parts[2].split("=")[1])  # Extract Median
                Min = float(parts[3].split("=")[1])  # Extract Min value
                Avg = float(parts[4].split("=")[1])  # Extract Avg value

                # Append values to lists
                data[U][test].append(compd)
                data[U]["Med"].append(Med)
                data[U]["Min"].append(Min)
                data[U]["Avg"].append(Avg)

    return data

# Group U values into bins of width 0.05 and compute averages
def group_and_average_data(data, bin_width=0.05):
    grouped_data = defaultdict(lambda: {test: [], "Med": [], "Min": [], "Avg": []})
    
    for U, values in data.items():
        bin_U = round(U / bin_width) * bin_width  # Assign to the nearest 0.05 bin
        grouped_data[bin_U][test].extend(values[test])
        grouped_data[bin_U]["Med"].extend(values["Med"])
        grouped_data[bin_U]["Min"].extend(values["Min"])
        grouped_data[bin_U]["Avg"].extend(values["Avg"])

    # Compute averages
    averaged_data = {
        U: {
            test: sum(values[test]) / len(values[test]) if values[test] else 0,
            "Med": sum(values["Med"]) / len(values["Med"]) if values["Med"] else 0,
            "Min": sum(values["Min"]) / len(values["Min"]) if values["Min"] else 0,
            "Avg": sum(values["Avg"]) / len(values["Avg"]) if values["Avg"] else 0,
        }
        for U, values in grouped_data.items()
    }

    return averaged_data

# Plot the results using scatter points and connecting lines
def plot_data_with_lines(data, bin_width=0.05):
    U_values = sorted(data.keys())  # Sorted bins for x-axis
    
    # Extract averaged values for each metric
    compd_values = [data[U][test] for U in U_values]
    Med_values = [data[U]["Med"] for U in U_values]
    Min_values = [data[U]["Min"] for U in U_values]
    Avg_values = [data[U]["Avg"] for U in U_values]

    plt.figure(figsize=(12, 6))

    # Plot with scatter points and connecting lines
    plt.plot(U_values, compd_values, linestyle='-', marker='o', label=test+" (Avg)", color='blue')
    plt.plot(U_values, Med_values, linestyle='--', marker='s', label="Med (Avg)", color='green')
    plt.plot(U_values, Min_values, linestyle='-', marker='^', label="Min (Avg)", color='orange')
    plt.plot(U_values, Avg_values, linestyle='-', marker='d', label="Avg (Avg)", color='purple')

    # Add a horizontal red line at y = 1 (Max reference)
    plt.axhline(y=1, color='red', linestyle='--', linewidth=1.5, label="Max = 1")

    # Labels and title
    plt.xlabel(f"U Value (Grouped in {bin_width} intervals)")
    plt.ylabel("Normalized Value (Averaged)")
    plt.title("Averaged Data for Different U Value Intervals (Scatter + Lines)")
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 3)
    # plt.ylim(0, 1.03)

    # Show plot
    plt.show()

# Main Execution
filename = "lackmus" + test + ".iu"  # Replace with your actual filename
raw_data = parse_and_average_data(filename)  # Parse raw data
binned_data = group_and_average_data(raw_data, bin_width=0.15)  # Group into bins
plot_data_with_lines(binned_data, bin_width=0.15)  # Plot with lines connecting points
