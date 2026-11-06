import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data
variants = ['Wild-Type', 'Y179C', 'Q388X', 'G396D', 'R19X']
affinities = [-5.52, -5.28, -4.98, -4.13, -1.23]
llr_scores = [0.0, 1.57, -float('inf'), -1.42, -float('inf')]  # We'll handle inf separately

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Binding Affinities
colors1 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
bars1 = ax1.bar(variants, affinities, color=colors1, edgecolor='black')
ax1.set_ylabel('Binding Affinity (kcal/mol)', fontsize=12)
ax1.set_title('Docking Results (AutoDock Vina)', fontsize=14, fontweight='bold')
ax1.set_ylim(-6.5, 0)
for bar, val in zip(bars1, affinities):
    ax1.text(bar.get_x() + bar.get_width()/2, val - 0.2, f'{val}', 
             ha='center', va='top', fontweight='bold', fontsize=11)

# Plot 2: ESM-2 LLR Scores
# Replace -inf with a very negative number for visualization
llr_plot = [-10 if np.isinf(x) else x for x in llr_scores]
colors2 = ['#1f77b4', '#2ca02c', '#9467bd', '#d62728', '#9467bd']
bars2 = ax2.bar(variants, llr_plot, color=colors2, edgecolor='black')
ax2.set_ylabel('ESM-2 LLR Score', fontsize=12)
ax2.set_title('Evolutionary Fitness (ESM-2)', fontsize=14, fontweight='bold')
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax2.set_ylim(-11, 5)
for bar, val in zip(bars2, llr_scores):
    text = '-inf' if np.isinf(val) else f'{val:.2f}'
    ypos = -10.5 if np.isinf(val) else val - 0.5
    ax2.text(bar.get_x() + bar.get_width()/2, ypos, text, 
             ha='center', va='top', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig('results/combined_analysis.png', dpi=300)
print("Combined plot saved to results/combined_analysis.png")