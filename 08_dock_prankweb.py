import os
import subprocess
from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation

DATA_DIR = "data"
RESULTS_DIR = "results_prankweb"
os.makedirs(RESULTS_DIR, exist_ok=True)

# 1. Prepare Ligand (8-oxoguanine) - same as before
smiles = "O=c1[nH]c(=O)c2[nH]c(N)nc2[nH]1"
print("Preparing 8-oxoguanine ligand...")
mol = Chem.MolFromSmiles(smiles)
mol = Chem.AddHs(mol)
AllChem.EmbedMolecule(mol, randomSeed=42)
preparator = MoleculePreparation()
preparator.prepare(mol)
ligand_pdbqt = os.path.join(DATA_DIR, "ligand_final.pdbqt")
preparator.write_pdbqt_file(ligand_pdbqt)
print("Ligand ready!")

# 2. Grid Box Settings (PrankWeb Pocket 1)
center_x = -2.79
center_y = 1.08
center_z = -9.55
size_x, size_y, size_z = 20, 20, 20  # Smaller box for a specific pocket

# 3. Find receptors
all_files = os.listdir(DATA_DIR)
proteins = [f for f in all_files if f.endswith("_receptor.pdbqt") and "R19X" not in f]

print(f"Found {len(proteins)} prepared receptor files.")

for prot_file in proteins:
    prot_name = prot_file.replace("_receptor.pdbqt", "")
    print(f"\n--- Docking {prot_name} into PrankWeb Pocket 1 ---")
    
    receptor = os.path.join(DATA_DIR, prot_file)
    out_file = os.path.join(RESULTS_DIR, f"{prot_name}_prankweb_docked.pdbqt")
    log_file = os.path.join(RESULTS_DIR, f"{prot_name}_prankweb_log.txt")

    command = [
        "vina.exe",
        "--receptor", receptor,
        "--ligand", ligand_pdbqt,
        "--center_x", str(center_x),
        "--center_y", str(center_y),
        "--center_z", str(center_z),
        "--size_x", str(size_x),
        "--size_y", str(size_y),
        "--size_z", str(size_z),
        "--out", out_file,
        "--exhaustiveness", "16"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)
            f.write(result.stderr)
        
        for line in result.stderr.split('\n'):
            if line.strip().startswith("1 "):
                print(f"Best affinity (PrankWeb pocket) for {prot_name}: {line.split()[1]} kcal/mol")
                break
    except subprocess.CalledProcessError as e:
        print(f"Error docking {prot_name}: {e.stderr}")

print("\nAll done! Check the 'results_prankweb' folder.")