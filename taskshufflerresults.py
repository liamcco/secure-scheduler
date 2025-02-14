import matplotlib.pyplot as plt
import numpy as np

# Read data from results.txt
# UTILIZATION,ENTROPY,NUM_OF_TASKS
data = np.genfromtxt("results.txt", delimiter=",", skip_header=1)

# Create a scatter plot
plt.scatter(data[:, 0], data[:, 1], c=data[:, 2], cmap='viridis')
plt.xlabel("Utilization")
plt.ylabel("Entropy")
plt.title("Utilization vs Entropy")
plt.colorbar(label="Number of Tasks")

# xlim and ylim
plt.xlim(0, 1)
plt.ylim(0, 8100)


plt.show()
