
import math
import numpy as np
from scipy.stats import t

def compute_cv_star(measurements):
    """
    from https://github.com/asbelz/coeff-var/blob/main/small_sample_cv.ipynb
    measurements: list or np.array of positive values
                  (study-level means or item-level means)
    returns: dict with CV*, mean, unbiased SD, CI, N
    """

    measurements = np.array(measurements, dtype=float)
    sample_size = len(measurements)

    if sample_size < 2:
        raise ValueError("Need at least 2 measurements for CV*")

    sample_mean = np.mean(measurements)
    if sample_mean <= 0:
        raise ValueError("Mean must be positive for CV")

    degrees_of_freedom = sample_size - 1

    # Unbiased sample variance
    sum_sq_diff = np.sum((measurements - sample_mean) ** 2)
    unbiased_var = sum_sq_diff / degrees_of_freedom
    corrected_sd = np.sqrt(unbiased_var)

    # c4(N) correction
    gamma_N_over_2 = math.gamma(sample_size / 2)
    gamma_df_over_2 = math.gamma(degrees_of_freedom / 2)
    c4_N = math.sqrt(2 / degrees_of_freedom) * gamma_N_over_2 / gamma_df_over_2

    unbiased_sd = corrected_sd / c4_N

    # CV and CV*
    cv = (unbiased_sd / sample_mean) * 100
    cv_star = (1 + (1 / (4 * sample_size))) * cv

    # SE and CI for SD
    se_var = unbiased_var * np.sqrt(2 / degrees_of_freedom)
    se_sd = se_var / (2 * unbiased_sd)
    ci_sd = t.interval(
        0.95,
        degrees_of_freedom,
        loc=unbiased_sd,
        scale=se_sd
    )

    return {
        "N": sample_size,
        "mean": sample_mean,
        "unbiased_sd": unbiased_sd,
        "cv_star": cv_star,
        "sd_ci_low": ci_sd[0],
        "sd_ci_high": ci_sd[1],
    }


# ============================================================
# Table printing helpers
# ============================================================
def md(df, title):
    print("\n# " + title)
    print(df.to_markdown(index=False))


def latex(df, caption, label, filename=None, verbose=False):
    lt = df.to_latex(index=False, caption=caption, label=label, float_format="%.4f")
    if filename is not None:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(lt)
    if verbose:
        print(lt)


def save_html_table(df, filename, caption=None):
    """
    Save a DataFrame as an HTML table suitable for copy-paste
    into Google Docs or Word.
    """
    html = df.to_html(index=False, border=1, justify="center")

    if caption is not None:
        html = f"<h3>{caption}</h3>\n" + html

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)