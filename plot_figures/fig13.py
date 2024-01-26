import matplotlib.pyplot as plt
import numpy as np

import json

with open("../experiments/mse_ideal_results.json") as f:
    results = json.load(f)


node_reductions = [
    results[f"aids_1"][0],
    results[f"imdb_1_small"][0],
    results[f"linux_1"][0],
]
edge_reductions = [
    results[f"aids_1"][1],
    results[f"imdb_1_small"][1],
    results[f"linux_1"][1],
]

colors = ["#DBE2EF", "#3F72AF", "#112D4E"]

group_labels = ["Aids", "IMDb", "Linux"]
bar_labels = ["Node Reduction Ratio", "Edge Reduction Ratio"]
# Calculate the mean and standard deviation for each group
bar1_values = [data[0] for data in node_reductions]
bar2_values = [data[0] for data in edge_reductions]
bar1_error = [data[1] for data in node_reductions]
bar2_error = [data[1] for data in edge_reductions]

# Setting up the plot
fig, ax = plt.subplots(figsize=(8, 5))
bar_width = 0.4
opacity = 1

# Positions of the bars
bar1_positions = np.arange(len(group_labels))
bar2_positions = [x + bar_width for x in bar1_positions]


# Plotting the bars with error bars
bar1 = plt.bar(
    bar1_positions,
    bar1_values,
    bar_width,
    alpha=opacity,
    color=colors[0],
    label=bar_labels[0],
    yerr=bar1_error,
    capsize=10,
    zorder=3,
    hatch="//",
)
bar2 = plt.bar(
    bar2_positions,
    bar2_values,
    bar_width,
    alpha=opacity,
    color=colors[1],
    label=bar_labels[1],
    yerr=bar2_error,
    capsize=10,
    zorder=3,
)

# Customizing the plot
# plt.xlabel('Graph Set', fontsize=18)
plt.ylabel("Reduction Ratio", fontsize=20)
plt.xticks(
    [r + bar_width / 2 for r in range(len(bar1_values))], group_labels, fontsize=20
)
plt.yticks(
    np.arange(0, 0.9, 0.2),
    ["{:.0%}".format(x) for x in np.arange(0, 0.9, 0.2)],
    fontsize=20,
)
plt.legend(fontsize=20)
plt.grid(axis="y", zorder=0, alpha=0.9)

plt.tight_layout()
plt.show()
