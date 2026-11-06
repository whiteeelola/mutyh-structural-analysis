import urllib.request
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

print("Downloading MUTYH sequence (Q9UIF7)...")
url = "https://rest.uniprot.org/uniprotkb/Q9UIF7.fasta"
response = urllib.request.urlopen(url)
fasta_data = response.read().decode('utf-8')
lines = fasta_data.split('\n')
wt_seq = "".join([l.strip() for l in lines[1:] if l.strip()])

print(f"Original sequence length: {len(wt_seq)}")

variants = {
    "wild_type": wt_seq,
    "R19X": wt_seq[:18],
    "Q388X": wt_seq[:387],
    "Y179C": wt_seq[:178] + 'C' + wt_seq[179:],
    "G396D": wt_seq[:395] + 'D' + wt_seq[396:]
}

for name, seq in variants.items():
    with open(os.path.join(DATA_DIR, f"{name}.fasta"), "w") as f:
        f.write(f">{name}\n{seq}\n")
    print(f"Saved {name}.fasta (Length: {len(seq)})")