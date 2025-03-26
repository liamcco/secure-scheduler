import matplotlib.pyplot as plt
import re

# Read and parse the data file
def parse_results(filename):
    data = {88: ([], []), 104: ([], []), 120: ([], [])}  # Dict to store f and E for each m
    
    with open(filename, 'r') as file:
        for line in file:
            match = re.search(r'n=(\d+),.*f=([0-9\.]+), E=([0-9\.]+)', line)
            if match:
                n = int(match.group(1))
                f = float(match.group(2))
                E = float(match.group(3))
                if n in data:
                    data[n][0].append(f)
                    data[n][1].append(E)
    
    return data

# Plot the results with a legend
def plot_results(data):
    plt.figure(figsize=(8, 6))

    for n, (f_values, E_values) in data.items():
        plt.scatter(f_values, E_values, alpha=0.6, label=f"n = {n}")

    plt.xlabel("X")
    plt.ylabel("E")
    plt.title("Schedule entropy for different X")
    plt.grid(True)
    plt.legend(title="Number of Tasks (m)")
    plt.show()

# Run the script
if __name__ == "__main__":
    data = parse_results("results_c.txt")
    plot_results(data)
