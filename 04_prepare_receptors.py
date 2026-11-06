import os
import subprocess

DATA_DIR = "data"
variants = ["wild_type", "R19X", "Q388X", "Y179C", "G396D"]

OBABEL = "obabel"

for name in variants:
    pdb_file = os.path.join(DATA_DIR, f"{name}.pdb")
    pdbqt_file = os.path.join(DATA_DIR, f"{name}_receptor.pdbqt")
    
    if not os.path.exists(pdb_file):
        print(f"Error: {pdb_file} not found!")
        continue
        
    print(f"Preparing {name} with OpenBabel (adding charges)...")
    # -xr: prepare receptor (removes water, adds charges)
    cmd = f'{OBABEL} "{pdb_file}" -O "{pdbqt_file}" -xr'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if os.path.exists(pdbqt_file):
        print(f"Success: {pdbqt_file} created.")
    else:
        print(f"Failed to create {pdbqt_file}.")
        print("Error:", result.stderr)

print("All receptors prepared!")