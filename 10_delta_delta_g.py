import matplotlib.pyplot as plt
import numpy as np

# Data
variants = ['Y179C', 'Q388X', 'G396D']

# ΔΔG values (mutant - WT)
# DNA pocket: WT = -6.23
dna_ddg = [-4.62 - (-6.23), -1.25 - (-6.23), -5.62 - (-6.23)]  # +1.61, +4.98, +0.61
# PrankWeb pocket: WT = -6.14
prankweb_ddg = [-5.04 - (-6.14), -4.57 - (-6.14), -5.30 - (-6.14)]  # +1.10, +1.57, +0.84

x = np.arange(len(variants))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))

# Bars for DNA pocket
bars1 = ax.bar(x - width/2, dna_ddg, width, label='DNA-Binding Pocket', color='#1f77b4', edgecolor='black')
# Bars for PrankWeb pocket
bars2 = ax.bar(x + width/2, prankweb_ddg, width, label='Catalytic Pocket (PrankWeb)', color='#ff7f0e', edgecolor='black')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:+.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

# Customize the plot
ax.set_ylabel('ΔΔG (kcal/mol)', fontsize=12)
ax.set_title('Impact of Mutations on Binding Affinity (ΔΔG vs Wild-Type)', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(variants, fontsize=12)
ax.legend(fontsize=10)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add interpretation text
ax.text(0.5, 0.95, 'Higher ΔΔG = Greater Loss of Binding', 
        transform=ax.transAxes, ha='center', fontsize=10, style='italic', color='grey')

plt.tight_layout()
plt.savefig('results/delta_delta_g.png', dpi=300)
print("Chart saved to results/delta_delta_g.png")