import matplotlib.pyplot as plt
import numpy as np

# Data
variants = ['Wild-Type', 'Y179C', 'Q388X', 'G396D']
dna_affinities = [-6.23, -4.62, -1.25, -5.62]
prankweb_affinities = [-6.14, -5.04, -4.57, -5.30]

x = np.arange(len(variants))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))

# Bars for DNA pocket
bars1 = ax.bar(x - width/2, dna_affinities, width, label='DNA-Binding Pocket (8FAY)', color='#1f77b4', edgecolor='black')
# Bars for PrankWeb pocket
bars2 = ax.bar(x + width/2, prankweb_affinities, width, label='Catalytic Pocket (PrankWeb)', color='#ff7f0e', edgecolor='black')

# Add value labels on top of bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

# Customize the plot
ax.set_ylabel('Binding Affinity (kcal/mol)', fontsize=12)
ax.set_title('Comparison of Binding Affinities: DNA-Interface vs Catalytic Pocket', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(variants, fontsize=12)
ax.legend(fontsize=10)
ax.set_ylim(-7.5, 0)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('results/pocket_comparison.png', dpi=300)
print("Chart saved to results/pocket_comparison.png")