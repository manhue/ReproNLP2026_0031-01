
import pandas as pd

# Load both Excel files
original_df = pd.read_excel("original_file.xlsx", engine="openpyxl")
merged_df = pd.read_excel("merged_readability_evaluation.xlsx", engine="openpyxl")

# Function to print summary statistics
def print_summary(name, df):
    print(f"\nSummary for {name}:")
    print(f"Total items: {len(df)}")

    for col in ["labeller_id", "source", "split", "story_name"]:
        print(f"\nItems per {col}:")
        print(df[col].value_counts())

    print("\nItems per labeller_id and source:")
    print(df.groupby(["labeller_id", "source"]).size())

    print("\nItems per labeller_id and story_name:")
    print(df.groupby(["labeller_id", "story_name"]).size())

    print("\nItems per labeller_id and split:")
    print(df.groupby(["labeller_id", "split"]).size())

    qa_id_counts = df["qa_id"].value_counts()
    print(qa_id_counts.value_counts())

# Run summaries
print_summary("========= Original File", original_df)
print_summary("\n\n========= Merged File", merged_df)

# Check that the two files except for the to-be-labelled column

# Column to ignore
ignore_columns_orig = ["readability(grammarly correct and clear language. worst 1 to 5)",  "relevancy_A(Answer can correctly answer the Q. 1 to 5)",  "relevancy_Q(Q is relevant to section. 1 to 5)"]
ignore_columns_merge = ["readability(grammarly correct and clear language. worst 1 to 5)"]

# Drop the column from both DataFrames
print(original_df.shape)
original_compare = original_df.drop(columns=ignore_columns_orig, errors="ignore")
print(original_df.shape)
merged_compare = merged_df.drop(columns=ignore_columns_merge, errors="ignore")

# Sort columns alphabetically for consistent comparison
original_compare = original_compare[sorted(original_compare.columns)]
merged_compare = merged_compare[sorted(merged_compare.columns)]

# Compare: rows in original not in merged
missing_in_merged = pd.concat([original_compare, merged_compare, merged_compare]).drop_duplicates(keep=False)

# Compare: rows in merged not in original
missing_in_original = pd.concat([merged_compare, original_compare, original_compare]).drop_duplicates(keep=False)

# Print summary
print("\n\n========= ✅ Comparison Summary:")
print(f"Total rows in original_file: {len(original_df)}")
print(f"Total rows in merged_file: {len(merged_df)}")
print(f"Rows missing in merged_file (excluding readability): {len(missing_in_merged)}")
print(f"Rows missing in original_file (excluding readability): {len(missing_in_original)}")

# Optional: print mismatches
if not missing_in_merged.empty:
    print("\n❌ Rows in original_file not found in merged_file:")
    print(missing_in_merged)

if not missing_in_original.empty:
    print("\n❌ Rows in merged_file not found in original_file:")
    print(missing_in_original)

