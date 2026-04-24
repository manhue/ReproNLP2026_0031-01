import pandas as pd

# Load the Excel file
df = pd.read_excel("original_file.xlsx", engine="openpyxl")

# Step 1: Remove specified columns
columns_to_remove = [
    "story_name",
    "section_id",
    "source",
    "split",
    "relevancy_Q(Q is relevant to section. 1 to 5)",
    "relevancy_A(Answer can correctly answer the Q. 1 to 5)"
]
df_cleaned = df.drop(columns=columns_to_remove)

# Step 2: Clear readability values
df_cleaned["readability(grammarly correct and clear language. worst 1 to 5)"] = ""


# Step 3: Split by labeller_id
labeller_groups = df_cleaned.groupby("labeller_id")

# Step 4: Create individual files
file_mapping = {}
for i, (labeller_id, group_df) in enumerate(labeller_groups):
    group_df = group_df.drop(columns=["labeller_id"])
    filename = f"qa_labeller_{labeller_id}.xlsx"
    group_df.to_excel(filename, index=False)
    file_mapping[labeller_id] = filename

