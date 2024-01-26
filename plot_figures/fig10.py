import matplotlib.pyplot as plt
import numpy as np

import json

with open("../experiments/mse_noisy_results.json") as f:
    results = json.load(f)

nodes = sorted([int(key) for key in results.keys()])

baseline_mse = [results[str(node)][0] for node in nodes]
red_qaoa_mse = [results[str(node)][1] for node in nodes]

colors = ["#DBE2EF", "#3F72AF", "#112D4E"]
# data
bar1 = baseline_mse
bar2 = red_qaoa_mse

# set up the figure
fig, ax = plt.subplots(figsize=(7, 4))

# set the font size
plt.rcParams.update({"font.size": 19})

# set bar width
bar_width = 0.35

# create the bar plots
r1 = np.arange(len(bar1))
r2 = [x + bar_width for x in r1]
# colors = ['red', 'green']
ax.bar(r1, bar1, width=bar_width, label="Baseline", color=colors[0], hatch="//")
ax.bar(r2, bar2, width=bar_width, label="Red-QAOA", color=colors[1])

# add xticks and labels
ax.set_xticks([r + bar_width / 2 for r in range(len(bar1))], nodes)

# add y-axis label and set limits
ax.set_ylabel("Noisy MSE")
ax.set_xlabel("Number of Qubits")

# add legend
ax.legend(loc="upper left", ncol=1, fontsize=16)

# add horizontal grid lines and put them to back
plt.grid(axis="y")
ax.set_axisbelow(True)

# format y-axis as percentage
fmt = "%.2f"
yticks = plt.yticks()[0]
plt.yticks(yticks, [fmt % y for y in yticks])

# show the plot
plt.tight_layout()
plt.show()
