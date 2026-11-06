import os
import subprocess
from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation

DATA_DIR = "data"
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# 1. Prepare Ligand (8-oxoguanine)
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

# 2. Grid Box Settings (DNA binding pocket from 8FAY)
center_x = 14.92
center_y = -9.18
center_z = -23.66
size_x, size_y, size_z = 25, 25, 25

# 3. Find receptors
all_files = os.listdir(DATA_DIR)
proteins = [f for f in all_files if f.endswith("_receptor.pdbqt") and "R19X" not in f]


print(f"Found {len(proteins)} prepared receptor files.")

for prot_file in proteins:
    prot_name = prot_file.replace("_receptor.pdbqt", "")
    print(f"\n--- Docking {prot_name} with 8-oxoG ---")
    
    receptor = os.path.join(DATA_DIR, prot_file)
    out_file = os.path.join(RESULTS_DIR, f"{prot_name}_final_docked.pdbqt")
    log_file = os.path.join(RESULTS_DIR, f"{prot_name}_final_log.txt")

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
                print(f"Best affinity for {prot_name}: {line.split()[1]} kcal/mol")
                break
    except subprocess.CalledProcessError as e:
        print(f"Error docking {prot_name}: {e.stderr}")

print("\nAll done! Check the 'results' folder.")