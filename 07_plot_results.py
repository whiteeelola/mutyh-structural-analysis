import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("results", exist_ok=True)

dock_variants = ['Wild-Type', 'Y179C', 'Q388X', 'G396D']
affinities = [-5.52, -5.28, -4.98, -4.13]

esm_variants = ['WT (Y179)', 'Y179C', 'WT (G396)', 'G396D', 'R19X', 'Q388X']
llr_scores = [0.0, 1.57, 0.0, -1.42, -float('inf'), -float('inf')]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

colors1 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
bars1 = ax1.bar(dock_variants, affinities, color=colors1, edgecolor='black', width=0.6)
ax1.set_ylabel('Binding Affinity (kcal/mol)', fontsize=12)
ax1.set_title('Focused Docking (Valid Cavities)', fontsize=13, fontweight='bold')
ax1.set_ylim(-6.5, 0)
for bar, val in zip(bars1, affinities):
    ax1.text(bar.get_x() + bar.get_width()/2, val - 0.15, f'{val}', 
             ha='center', va='top', fontweight='bold', fontsize=10)

llr_plot = [-8 if np.isinf(x) else x for x in llr_scores]
colors2 = ['#1f77b4', '#ff7f0e', '#1f77b4', '#d62728', '#7f7f7f', '#7f7f7f']
bars2 = ax2.bar(esm_variants, llr_plot, color=colors2, edgecolor='black', width=0.6)
ax2.set_ylabel('ESM-2 LLR Score', fontsize=12)
ax2.set_title('Evolutionary Fitness (ESM-2 LLRs)', fontsize=13, fontweight='bold')
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax2.set_ylim(-9, 3)

for bar, val in zip(bars2, llr_scores):
    text = '-inf' if np.isinf(val) else f'{val:.2f}'
    ypos = -7.8 if np.isinf(val) else (val + 0.15 if val >= 0 else val - 0.4)
    va_dir = 'bottom' if val >= 0 and not np.isinf(val) else 'top'
    ax2.text(bar.get_x() + bar.get_width()/2, ypos, text, 
             ha='center', va=va_dir, fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('results/combined_analysis.png', dpi=300)
print("Updated plot saved to results/combined_analysis.png")