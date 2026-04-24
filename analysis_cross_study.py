import pandas as pd
from itertools import combinations
from scipy.stats import pearsonr, spearmanr
from utils import compute_cv_star, latex, md, save_html_table

"""
    Compare the four evaluations:
        - Yao et al. 2022 (original study)
        - Florescu et al. 2024
        - Braun 2025
        - Reproduction 2026 (ours)
        
    For each of these, we have mean ratings per system (and standard deviations).
        
"""

sets_of_sets_of_measurements = {
    "Reproduction2026": {
        "groundtruth": {"mean": 4.18182, "std": 0.989572},
        "Ours": {"mean": 3.59583, "std": 1.53862},
        "PAQ": {"mean": 3.25, "std": 1.62228},
    },
    "Yao2022": {
        "groundtruth": {"mean": 4.95, "std": 0.28},
        "Ours": {"mean": 4.71, "std": 0.70},
        "PAQ": {"mean": 4.08, "std": 1.13},
    },
    "Florescu": {
        "groundtruth": {"mean": 4.71, "std": 0.52},
        "Ours": {"mean": 4.52, "std": 0.75},
        "PAQ": {"mean": 4.17, "std": 1.22},
    },
    "Braun": {
        "groundtruth": {"mean": 4.38, "std": 0.96},
        "Ours": {"mean": 3.85, "std": 1.35},
        "PAQ": {"mean": 3.14, "std": 1.43},
    }
}


def compute_means_based_cv_star(study_data):
    rows = []

    systems = list(next(iter(study_data.values())).keys())

    for system in systems:
        measurements = [
            study_data[study][system]["mean"]
            for study in study_data
        ]

        cv_stats = compute_cv_star(measurements)
        rows.append({
            "system": system,
            **cv_stats
        })

    return pd.DataFrame(rows)


# COEFFICIENT OF VARIATION ON SYSTEM MEANS
rows = []

systems = list(next(iter(sets_of_sets_of_measurements.values())).keys())

for system in systems:
    measurements = [
        sets_of_sets_of_measurements[study][system]["mean"]
        for study in sets_of_sets_of_measurements
    ]

    cv_stats = compute_cv_star(measurements)
    rows.append({
        "system": system,
        **cv_stats
    })

means_cv_df = pd.DataFrame(rows)

md(
    means_cv_df,
    "Means-based CV* across four studies"
)

latex(
    means_cv_df,
    caption="Means-based small-sample bias-corrected coefficient of variation (CV*) across four studies.",
    label="tab:cv-means",
    filename="tables/coeff_variation_means_based.latex.txt"
)

save_html_table(
    means_cv_df,
    "tables/coeff_variation_means_based.html",
    caption="Means-based CV* across four evaluation studies"
)


# COEFFICIENT OF VARIATION ON SYSTEM MEANS - OUR REPRO VS YAO ET AL
rows = []

systems = list(next(iter(sets_of_sets_of_measurements.values())).keys())

for system in systems:
    measurements = [
        sets_of_sets_of_measurements[study][system]["mean"]
        for study in ["Reproduction2026", "Yao2022"]
    ]

    cv_stats = compute_cv_star(measurements)
    rows.append({
        "system": system,
        **cv_stats
    })

means_cv_df_ours_vs_orig = pd.DataFrame(rows)

md(
    means_cv_df_ours_vs_orig,
    "Means-based CV* comparing our evaluation and the original study"
)

latex(
    means_cv_df,
    caption="Means-based small-sample bias-corrected coefficient of variation (CV*) comparing the original study and our reproduction.",
    label="tab:cv-means",
    filename="tables/coeff_variation_means_based___ours_vs_orig.latex.txt"
)

save_html_table(
    means_cv_df,
    "tables/coeff_variation_means_based_ours_vs_orig.html",
    caption="Means-based CV* comparing the original study and our reproduction."
)

# CORRELATIONS ON SYSTEM MEANS
rows = []
for study, systems in sets_of_sets_of_measurements.items():
    for system, vals in systems.items():
        if vals["mean"] is None: continue
        rows.append([study, system, vals['mean'], vals['std']])

means_df = pd.DataFrame(rows, columns=["Study", "System", "Mean", "SD"])
wide_mean = means_df.pivot(index="Study", columns="System", values="Mean")
#wide_sd = means_cv_df.pivot(index="Study", columns="System", values="SD")

pearson_rows = []
spearman_rows = []

for s1, s2 in combinations(wide_mean.columns, 2):
    r, p = pearsonr(wide_mean[s1], wide_mean[s2])
    rs, ps = spearmanr(wide_mean[s1], wide_mean[s2])
    pearson_rows.append([s1, s2, r, p])
    spearman_rows.append([s1, s2, rs, ps])

pearson_df = pd.DataFrame(pearson_rows, columns=["System 1", "System 2", "r", "p"])
spearman_df = pd.DataFrame(spearman_rows, columns=["System 1", "System 2", "rho", "p"])

md(pearson_df, "Pearson Correlations")
latex(pearson_df, "Pearson correlations across studies.", "tab:pearson",
      filename="tables/pearson_across_studies.latex.txt")
save_html_table(
    pearson_df,
    "tables/pearson_across_studies.html",
    caption="Pearson correlations across studies"
)

md(spearman_df, "Spearman Correlations")
latex(spearman_df, "Spearman correlations across studies.", "tab:spearman",
      filename="tables/spearman_across_studies.latex.txt")

save_html_table(
    spearman_df,
    "tables/spearman_across_studies.html",
    caption="Spearman correlations across studies"
)
