import matplotlib.pyplot as plt

# Read delays
with open("results.txt", "r") as f:
    delays = [float(line.strip()) for line in f]

# X-axis (sample number)
x = list(range(len(delays)))

# Plot
plt.plot(x, delays)
plt.xlabel("Request Number")
plt.ylabel("Delay (seconds)")
plt.title("Delay vs Requests")

plt.savefig("performance_graph.png")