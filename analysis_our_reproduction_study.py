import pandas as pd
import numpy as np
import krippendorff
from itertools import combinations
from scipy.stats import ttest_ind
from utils import latex, md, save_html_table

rating_col = "readability(grammarly correct and clear language. worst 1 to 5)"
system_col = "source"
rater_col = "labeller_id"
item_col = "qa_id"


# ============================================================
# Compute Krippendorff α using the Castro implementation
# ============================================================
def compute_alpha_from_pivot(pivot):
    """
    pivot: rows = items, columns = raters
    """
    data = pivot.to_numpy().T   # krippendorff expects coders × units
    return krippendorff.alpha(reliability_data=data, level_of_measurement="ordinal")


# ============================================================
# Pairwise α per rater pair
# ============================================================
def pairwise_alpha(df):
    pivot = df.pivot_table(
        index=item_col,
        columns=rater_col,
        values=rating_col
    )

    rows = []

    for r1, r2 in combinations(pivot.columns, 2):
        sub = pivot[[r1, r2]]

        # Keep only items annotated by BOTH raters
        sub = sub.dropna()

        n_shared = len(sub)

        # Krippendorff's alpha is undefined without overlap
        if n_shared < 1:
            continue

        data = sub.to_numpy().T
        alpha = krippendorff.alpha(
            reliability_data=data,
            level_of_measurement="ordinal"
        )

        rows.append([r1, r2, n_shared, alpha])

    alpha_df = pd.DataFrame(
        rows,
        columns=["Rater 1", "Rater 2", "Shared items", "Alpha"]
    )

    md(alpha_df, "Pairwise Krippendorff’s Alpha (Ordinal)")
    latex(alpha_df,
          caption="Pairwise Krippendorff’s α for all rater pairs (ordinal).",
          label="tab:pairwise-alpha",
          filename="tables/pairwise_alpha_current_study.latex.txt")
    save_html_table(
        alpha_df,
        "tables/pairwise_alpha_current_study.html",
        caption="Pairwise Krippendorff’s alpha (ordinal, overlapping raters)"
    )

    return alpha_df


# ============================================================
# MAIN EXECUTION
# ============================================================
if __name__ == "__main__":

    df = pd.read_excel("Evaluation_interface_spreadsheets/merged_readability_evaluation.xlsx", engine="openpyxl")

    # MEANS + STDs
    stats = df.groupby(system_col)[rating_col].agg(['mean', 'std']).reset_index()
    md(stats, "Means and Standard Deviations")
    latex(stats, "Means and standard deviations for the current study.", "tab:means", filename="tables/means_sds_current_study.latex.txt")
    save_html_table(
        stats,
        "tables/means_sds_current_study.html",
        caption="Means and standard deviations for the current study"
    )


    # OVERALL α
    pivot = df.pivot_table(index=item_col, columns=rater_col, values=rating_col)
    overall_alpha = compute_alpha_from_pivot(pivot)
    print("\n## Overall Krippendorff’s Alpha (ordinal):", overall_alpha)

    # α PER SYSTEM
    rows = []
    for sys in df[system_col].unique():
        sub = df[df[system_col] == sys]
        pivot_sys = sub.pivot_table(index=item_col, columns=rater_col, values=rating_col)
        a = compute_alpha_from_pivot(pivot_sys)
        rows.append([sys, a])

    alpha_system_df = pd.DataFrame(rows, columns=["System", "Alpha"])
    md(alpha_system_df, "Alpha per System")
    latex(alpha_system_df, "Per-system Krippendorff’s α.", "tab:alpha-system", filename="tables/alpha_per_system_current_study.latex.txt")
    save_html_table(
        alpha_system_df,
        "tables/alpha_per_system_current_study.html",
        caption="Krippendorff’s alpha per system (ordinal)"
    )

    # PAIRWISE α
    pairwise_alpha(df)

    # T-TESTS
    systems = df[system_col].unique()
    rows = []
    for s1, s2 in combinations(systems, 2):
        r1 = df[df[system_col] == s1][rating_col]
        r2 = df[df[system_col] == s2][rating_col]
        t, p = ttest_ind(r1, r2, equal_var=False)
        rows.append([s1, s2, t, p])

    t_df = pd.DataFrame(rows, columns=["System 1", "System 2", "t", "p"])
    md(t_df, "Pairwise t-tests")
    latex(t_df, "Pairwise t-tests between systems.", "tab:t-tests", filename="tables/pairwise_ttests_current_study.latex.txt",
)
    save_html_table(
        t_df,
        "tables/pairwise_ttests_current_study.html",
        caption="Pairwise t-tests between systems"
    )
