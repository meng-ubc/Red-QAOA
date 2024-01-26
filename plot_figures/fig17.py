import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib


with open("../experiments/end_to_end_results.json", "r") as file:
    results = json.load(file)

bar_values = []
bar_errors = []

for p in range(1, 4):
    key = str(p)
    bar_values.append(
        [
            results[key][0][0],
            results[key][1][0],
        ]
    )
    bar_errors.append(
        [
            results[key][0][1],
            results[key][1][1],
        ]
    )

plt.rcParams.update({"font.size": 16})
# Setting up the figure and axes
fig, ax = plt.subplots(figsize=(6, 4))
colors = ["#DBE2EF", "#3F72AF", "#112D4E"]

# Define bar positions and width
bar_width = 0.25
indices = np.arange(2)  # Two bars: min_ratio and mean_ratio

hatches = ["/", "", "\\"]
# Plotting the bars for each p value
for i, p in enumerate(range(1, 4)):
    ax.bar(
        indices + i * bar_width,
        bar_values[i],
        bar_width,
        label=f"p = {p}",
        yerr=bar_errors[i],
        capsize=8,
        color=colors[i],
        zorder=3,
        hatch=hatches[i],
    )

# Setting titles, labels, and legend
ax.set_xticks(indices + bar_width)
ax.set_xticklabels(
    ["Best Result\n(Optimal Restart)", "Average Result\n(Across All Restarts)"]
)

ax.set_ylabel("Red-QAOA / Baseline Ratio")
ax.legend(title="QAOA Layers")

ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.22))

ax.set_ylim(0.6, 1.07)

ax.grid(axis="y", which="both", zorder=0)

# Adding annotations (Optional)
for i, p in enumerate(ax.patches):
    offset = 0.01
    if i % 2 == 1:
        offset += 0.04

    height = p.get_height()
    ax.annotate(
        f"{height:.2f}",
        xy=(p.get_x() + p.get_width() / 2, height + offset),
        ha="center",
        va="bottom",
    )

# Automatically adjust subplot to fit figure area
plt.tight_layout()
plt.show()
