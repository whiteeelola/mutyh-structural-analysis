import json
import os

DATA_DIR = "data"
variants = ["wild_type", "R19X", "Q388X", "Y179C", "G396D"]
jobs = []

for name in variants:
    with open(os.path.join(DATA_DIR, f"{name}.fasta"), "r") as f:
        lines = f.readlines()
        seq = "".join([l.strip() for l in lines if not l.startswith(">")])
    
    job = {
        "name": f"MUTYH_{name}",
        "modelSeeds": [],
        "sequences": [{"proteinChain": {"sequence": seq, "count": 1}}],
        "dialect": "alphafoldserver",
        "version": 1
    }
    jobs.append(job)

with open(os.path.join(DATA_DIR, "af3_jobs.json"), "w") as f:
    json.dump(jobs, f, indent=2)

print("JSON created: data/af3_jobs.json")