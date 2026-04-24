
import pandas as pd
import glob
import re

# Load the original full spreadsheet
original_df = pd.read_excel("original_file.xlsx", engine="openpyxl")

# Drop excluded columns
excluded_columns = [
    "relevancy_Q(Q is relevant to section. 1 to 5)",
    "relevancy_A(Answer can correctly answer the Q. 1 to 5)"
]
original_df = original_df.drop(columns=[col for col in excluded_columns if col in original_df.columns])

# Load and clean all reduced spreadsheets
reduced_files = glob.glob("qa_labeller_*_completed.xlsx")
merged_dfs = []

for file in reduced_files:
    # Extract labeller_id from filename
    match = re.search(r"qa_labeller_(\d+)_completed\.xlsx", file)
    if not match:
        print(f"⚠️ Filename format incorrect: {file}")
        continue
    file_labeller_id = int(match.group(1))

    # Load reduced file
    df = pd.read_excel(file, engine="openpyxl")
    df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed|^\d+$")]

    # Add labeller_id from filename
    df["labeller_id"] = file_labeller_id

    # Filter original_df to match both qa_id and labeller_id
    original_subset = original_df[
        (original_df["labeller_id"] == file_labeller_id) &
        (original_df["qa_id"].isin(df["qa_id"]))
    ]

    # Identify columns to merge (excluding readability)
    readability_col = "readability(grammarly correct and clear language. worst 1 to 5)"
    columns_to_merge = [col for col in original_subset.columns if col not in df.columns and col != readability_col]

    # Merge on qa_id and labeller_id
    merged = pd.merge(df, original_subset[["qa_id", "labeller_id"] + columns_to_merge], on=["qa_id", "labeller_id"], how="left")

    merged_dfs.append(merged)

# Combine all merged data
final_df = pd.concat(merged_dfs, ignore_index=True)

# Save final merged file
final_df.to_excel("merged_readability_evaluation.xlsx", index=False)

print("✅ Merged file saved as 'merged_readability_evaluation.xlsx'")
