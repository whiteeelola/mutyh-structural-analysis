import os
import torch
from transformers import AutoTokenizer, EsmForMaskedLM
import pandas as pd

DATA_DIR = "data"

# 1. Load ESM-2 model
print("Loading ESM-2 model (this may take a minute)...")
model_name = "facebook/esm2_t6_8M_UR50D"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = EsmForMaskedLM.from_pretrained(model_name)
model.eval()

# 2. Load sequences
variants = {
    "Wild-Type": "wild_type",
    "R19X": "R19X",
    "Q388X": "Q388X",
    "Y179C": "Y179C",
    "G396D": "G396D"
}

results = []

for name, filename in variants.items():
    fasta_path = os.path.join(DATA_DIR, f"{filename}.fasta")
    if not os.path.exists(fasta_path):
        print(f"Skipping {name}: {fasta_path} not found.")
        continue
    
    with open(fasta_path, "r") as f:
        lines = f.readlines()
        seq = "".join([l.strip() for l in lines if not l.startswith(">")])
    
    # For simplicity, we only analyze the first 100 amino acids for truncated proteins
    # or the specific mutation site for point mutations.
    if len(seq) <= 20:  # R19X
        pos = len(seq) - 1  # Last residue
        wt_aa = seq[pos]
        mut_aa = "X"  # Stop codon
        masked_seq = seq[:pos] + "<mask>" + seq[pos+1:]
    elif len(seq) < 400:  # Q388X
        pos = len(seq) - 1
        wt_aa = seq[pos]
        mut_aa = "X"
        masked_seq = seq[:pos] + "<mask>" + seq[pos+1:]
    else:
        # For point mutations, we analyze the specific position
        if name == "Y179C":
            pos = 178
            wt_aa = "Y"
            mut_aa = "C"
        elif name == "G396D":
            pos = 395
            wt_aa = "G"
            mut_aa = "D"
        else:
            # For Wild-Type, we just take a random position to show it's normal
            pos = 100
            wt_aa = seq[pos]
            mut_aa = wt_aa  # No mutation
        masked_seq = seq[:pos] + "<mask>" + seq[pos+1:]
    
    # Tokenize and predict
    inputs = tokenizer(masked_seq, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits[0, 1, :]
    log_probs = torch.log_softmax(logits, dim=-1)
    
    # Get log probabilities for WT and mutant
    wt_token_id = tokenizer.convert_tokens_to_ids(wt_aa)
    wt_log_prob = log_probs[wt_token_id].item()
    
    if mut_aa in ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y"]:
        mut_token_id = tokenizer.convert_tokens_to_ids(mut_aa)
        mut_log_prob = log_probs[mut_token_id].item()
        llr = mut_log_prob - wt_log_prob
    else:
        llr = float('-inf')  # Stop codon is catastrophic
    
    results.append({
        "Variant": name,
        "WT_Amino_Acid": wt_aa,
        "Mutant_Amino_Acid": mut_aa,
        "Position": pos + 1,
        "LLR_Score": llr
    })
    print(f"{name}: Position {pos+1}, WT={wt_aa}, Mut={mut_aa}, LLR={llr:.4f}")

# 3. Save results
df = pd.DataFrame(results)
df.to_csv(os.path.join(DATA_DIR, "esm2_results.csv"), index=False)
print("\nResults saved to data/esm2_results.csv")
print(df)