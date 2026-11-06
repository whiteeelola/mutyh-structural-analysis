import os
import torch
from transformers import AutoTokenizer, EsmForMaskedLM
import pandas as pd

DATA_DIR = "data"

print("Loading ESM-2 model...")
model_name = "facebook/esm2_t6_8M_UR50D"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = EsmForMaskedLM.from_pretrained(model_name)
model.eval()

with open(os.path.join(DATA_DIR, "wild_type.fasta"), "r") as f:
    wt_seq = "".join([l.strip() for l in f.readlines() if not l.startswith(">")])

mutations = [
    {"Variant": "Wild-Type (Ref 179)", "pos": 178, "wt_aa": "Y", "mut_aa": "Y"},
    {"Variant": "Wild-Type (Ref 396)", "pos": 395, "wt_aa": "G", "mut_aa": "G"},
    {"Variant": "Y179C", "pos": 178, "wt_aa": "Y", "mut_aa": "C"},
    {"Variant": "G396D", "pos": 395, "wt_aa": "G", "mut_aa": "D"},
    {"Variant": "R19X", "pos": 18, "wt_aa": "R", "mut_aa": "X"},
    {"Variant": "Q388X", "pos": 387, "wt_aa": "Q", "mut_aa": "X"}
]

results = []

for mut in mutations:
    pos = mut["pos"]
    wt_aa = mut["wt_aa"]
    mut_aa = mut["mut_aa"]
    name = mut["Variant"]

    masked_seq = wt_seq[:pos] + "<mask>" + wt_seq[pos+1:]
    
    inputs = tokenizer(masked_seq, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    mask_token_index = torch.where(inputs["input_ids"] == tokenizer.mask_token_id)[1].item()
    logits = outputs.logits[0, mask_token_index, :]
    log_probs = torch.log_softmax(logits, dim=-1)
    
    wt_token_id = tokenizer.convert_tokens_to_ids(wt_aa)
    wt_log_prob = log_probs[wt_token_id].item()
    
    if mut_aa in tokenizer.get_vocab() and mut_aa != "X":
        mut_token_id = tokenizer.convert_tokens_to_ids(mut_aa)
        mut_log_prob = log_probs[mut_token_id].item()
        llr = mut_log_prob - wt_log_prob
    else:
        llr = float('-inf')
        
    results.append({
        "Variant": name,
        "WT_Amino_Acid": wt_aa,
        "Mutant_Amino_Acid": mut_aa,
        "Position": pos + 1,
        "LLR_Score": llr
    })
    print(f"{name}: Position {pos+1}, {wt_aa}->{mut_aa}, LLR={llr:.4f}")

df = pd.DataFrame(results)
df.to_csv(os.path.join(DATA_DIR, "esm2_results.csv"), index=False)
print("\nResults saved to data/esm2_results.csv")