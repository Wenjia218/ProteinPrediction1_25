import pandas as pd
import ast
import re
from datasets import load_from_disk


# Load the files
df_af = pd.read_csv("data/AlphaFold_pLDDT.csv")
df_at = pd.read_csv("data/ATLAS_plddt_rmsf_bfactors.csv")

# Parse list values
df_af["pLDDT"] = df_af["pLDDT"].apply(ast.literal_eval)
df_af["pdb_id"] = df_af["pdb_id"].str.lower()

df_at["rmsf_values"] = df_at["rmsf_values"].apply(ast.literal_eval)
df_at["pdb_id"] = df_at["pdb_id"].str.split("_").str[0]
df_at.drop(columns=["plddt_values"], inplace=True)
df_at.drop(columns=["bfactors"], inplace=True)

bfactor_dataset = load_from_disk("rawdata/SoftDis/clusters_arrow")
softdis = bfactor_dataset.to_pandas()

softdis["pdb_id"] = softdis["id"].str.split("_").str[0]
softdis.drop(columns=["id"], inplace=True)

# === Merge all three and keep rows with equal-length lists ===
merged = df_af.merge(df_at, on="pdb_id").merge(softdis, on="pdb_id")
merged_filtered = merged[["pdb_id", "pLDDT", "rmsf_values", "bfactors"]]
merged_filtered.columns = ["pdb_id", "plddt_alphafold", "rmsf_atlas", "bfactors_softdis"]

print(merged_filtered.columns)
print(len(merged_filtered))

merged_filtered.to_csv("outputs/merged_disorder_scores.csv", index=False)

'''
def equal_length(row):
    return len(row["pLDDT"]) == len(row["rmsf_values"]) == len(row["bfactors_y"])

merged_filtered = merged[merged.apply(equal_length, axis=1)].copy()

# Final output

merged_filtered.to_csv("outputs/merged_disorder_scores.csv", index=False)
print(f"✅ Done. Saved {len(merged_filtered)} valid entries to 'merged_disorder_scores.csv'.")
'''
