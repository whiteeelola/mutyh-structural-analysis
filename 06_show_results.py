import os

RESULTS_DIR = "results"

print("=== FINAL DOCKING RESULTS ===\n")

for filename in os.listdir(RESULTS_DIR):
    if filename.endswith("_final_log.txt"):
        protein_name = filename.replace("_final_log.txt", "")
        filepath = os.path.join(RESULTS_DIR, filename)
        
        # Read the log file
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Find the best affinity
        best_affinity = None
        for line in lines:
            if line.strip().startswith("1 "):
                # The line looks like: "   1       -9.12          0          0"
                parts = line.split()
                if len(parts) >= 2:
                    best_affinity = parts[1]
                    break
        
        if best_affinity:
            print(f"{protein_name:20s} : {best_affinity} kcal/mol")
        else:
            print(f"{protein_name:20s} : [Not found in log]")

print("\n=============================")