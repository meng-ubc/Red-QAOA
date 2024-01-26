import matplotlib.pyplot as plt
import numpy as np

import json


with open("../experiments/mse_ideal_results.json") as f:
    results = json.load(f)

bar_values = []
bar_errors = []

for p in range(1, 4):
    bar_values.append(
        [
            results[f"aids_{p}"][2][0],
            results[f"imdb_{p}_small"][2][0],
            results[f"linux_{p}"][2][0],
        ]
    )
    bar_errors.append(
        [
            results[f"aids_{p}"][2][1],
            results[f"imdb_{p}_small"][2][1],
            results[f"linux_{p}"][2][1],
        ]
    )


group_labels = ["Aids", "IMDb", "Linux"]
bar_labels = ["p=1", "p=2", "p=3"]

# Setting up the plot
fig, ax = plt.subplots(figsize=(8, 5))
bar_width = 0.25
opacity = 1
colors = ["#DBE2EF", "#3F72AF", "#112D4E"]
# Positions of the bars
bar1_positions = np.arange(len(group_labels))
bar2_positions = [x + bar_width for x in bar1_positions]
bar3_positions = [x + 2 * bar_width for x in bar1_positions]


# Plotting the bars with error bars
bar1 = plt.bar(
    bar1_positions,
    bar_values[0],
    bar_width,
    alpha=opacity,
    color=colors[0],
    label=bar_labels[0],
    yerr=bar_errors[0],
    capsize=4,
    zorder=3,
    hatch="//",
)
bar2 = plt.bar(
    bar2_positions,
    bar_values[1],
    bar_width,
    alpha=opacity,
    color=colors[1],
    label=bar_labels[1],
    yerr=bar_errors[1],
    capsize=4,
    zorder=3,
)
bar3 = plt.bar(
    bar3_positions,
    bar_values[2],
    bar_width,
    alpha=opacity,
    color=colors[2],
    label=bar_labels[2],
    yerr=bar_errors[2],
    capsize=4,
    zorder=3,
    hatch="\\",
)

# Customizing the plot
# plt.xlabel('Graph Set', fontsize=18)
plt.ylabel("MSE", fontsize=20)
plt.xticks(
    [r + bar_width for r in range(len(bar_values[0]))], group_labels, fontsize=20
)
plt.yticks(np.arange(0, 0.07, 0.02), fontsize=20)
plt.legend(fontsize=20)
plt.grid(axis="y", zorder=0, alpha=0.9)

# Saving the plot as a high-resolution image for publication
plt.tight_layout()
plt.show()
