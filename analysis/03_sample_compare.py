"""
03_sample_compare.py
====================

Pairwise (w0, wa) tension between the three SNe samples.

If the three SNe compilations were noisy realizations of the same underlying
(w0, wa) cosmology, their posterior means should agree within their combined
errors. Large pairwise tension means at least one of:
  (a) sample-specific systematics (calibration, selection, photometry),
  (b) genuine sample-specific physics signal,
  (c) the joint (w0, wa) preference is being driven differently by
      different parts of the z range each sample covers.

What we compute
---------------
For each pair (A, B), with mean mu_A, cov C_A and mean mu_B, cov C_B :

    d              = mu_A - mu_B
    C_combined     = C_A + C_B
    chi^2_pair     = d^T C_combined^{-1} d
    p_value        = 1 - F_{chi2, dof=2}(chi^2_pair)
    n_sigma        = sqrt(2) * erfcinv(p_value)

CAVEAT
------
C_A and C_B share DESI BAO + Planck + ACT lensing. The two posteriors are
NOT independent. C_A + C_B therefore OVERESTIMATES the variance of the
difference, so the n_sigma reported here is a CONSERVATIVE LOWER BOUND on
the actual tension. If even this lower bound is large (>= 2 sigma), the
samples disagree meaningfully. If it's small (< 1 sigma), they're
consistent under any treatment of the shared correlation.

USAGE
-----
    python analysis/03_sample_compare.py
    python analysis/03_sample_compare.py | more
"""

from __future__ import annotations

import importlib.util
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.stats import chi2 as chi2_dist
from scipy.special import erfcinv


# --- Import load + moments from 02_chain_load.py without renaming it. -------
# (Filenames starting with a digit can't be imported with a normal
#  `import 02_chain_load` statement, so we go through importlib.)
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "chain_load", HERE / "02_chain_load.py"
)
chain_load = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chain_load)

load_combo = chain_load.load_combo
weighted_moments = chain_load.weighted_moments
SAMPLES = chain_load.SAMPLES
CHAINS_ROOT = chain_load.CHAINS_ROOT
BURN_IN_FRACTION = chain_load.BURN_IN_FRACTION


# -----------------------------------------------------------------------------
# Pretty-print helpers
# -----------------------------------------------------------------------------

def banner(text: str, char: str = "=") -> None:
    print()
    print(char * 72)
    print(text)
    print(char * 72)


def matprint(label: str, M: np.ndarray, fmt: str = "{:+.6f}") -> None:
    print(f"  {label} =")
    for row in M:
        print("    [ " + "  ".join(fmt.format(x) for x in row) + " ]")


def vecprint(label: str, v: np.ndarray, fmt: str = "{:+.6f}") -> None:
    print(f"  {label} = [ " + "  ".join(fmt.format(x) for x in v) + " ]")


LINE = "-" * 72


# -----------------------------------------------------------------------------
# Pairwise tension
# -----------------------------------------------------------------------------

def tension(name_a: str, mu_a: np.ndarray, C_a: np.ndarray,
            name_b: str, mu_b: np.ndarray, C_b: np.ndarray) -> dict:

    banner(f"PAIR: {name_a}  vs  {name_b}", char="-")

    print("STEP 1  Means and covariances side by side")
    print(LINE)
    print(f"  {name_a}")
    vecprint("    mean", mu_a)
    matprint("    cov ", C_a)
    print(f"  {name_b}")
    vecprint("    mean", mu_b)
    matprint("    cov ", C_b)
    print()

    print("STEP 2  Difference vector d = mean_A - mean_B")
    print(LINE)
    d = mu_a - mu_b
    vecprint("d", d)
    print(f"  d[0] = w0_A - w0_B   = {d[0]:+.4f}")
    print(f"  d[1] = wa_A - wa_B   = {d[1]:+.4f}")
    print()

    print("STEP 3  Combined covariance C_combined = C_A + C_B")
    print(LINE)
    C = C_a + C_b
    matprint("C_combined", C)
    print(f"  det = {np.linalg.det(C):.4e}")
    print()

    print("STEP 4  chi^2_pair = d^T C_combined^{-1} d")
    print(LINE)
    Cinv = np.linalg.inv(C)
    matprint("C_combined^{-1}", Cinv, fmt="{:+.3f}")
    chi2_val = float(d @ Cinv @ d)
    # Manual expansion for inspection
    a = Cinv[0, 0] * d[0] ** 2
    b = 2 * Cinv[0, 1] * d[0] * d[1]
    c = Cinv[1, 1] * d[1] ** 2
    print(f"  term1: C^{{-1}}[0,0] * d[0]^2          = {a:+.4f}")
    print(f"  term2: 2 * C^{{-1}}[0,1] * d[0]*d[1]   = {b:+.4f}")
    print(f"  term3: C^{{-1}}[1,1] * d[1]^2          = {c:+.4f}")
    print(f"  sum = chi^2_pair                       = {a+b+c:+.4f}")
    print()

    print("STEP 5  p-value and equivalent n_sigma (2 dof)")
    print(LINE)
    p_value = float(chi2_dist.sf(chi2_val, df=2))
    n_sigma = float(np.sqrt(2) * erfcinv(p_value))
    print(f"  p-value = chi2.sf({chi2_val:.4f}, df=2) = {p_value:.4e}")
    print(f"  n_sigma = sqrt(2)*erfcinv(p)            = {n_sigma:.3f}")
    print()

    print("STEP 6  Interpretation")
    print(LINE)
    if n_sigma < 1.0:
        verdict = "CONSISTENT (lower bound; samples agree)"
    elif n_sigma < 2.0:
        verdict = "WEAK TENSION (lower bound; suggestive, not decisive)"
    elif n_sigma < 3.0:
        verdict = "TENSION (lower bound; samples meaningfully disagree)"
    else:
        verdict = "STRONG TENSION (lower bound; deep disagreement)"
    print(f"  {verdict}")
    print(f"  REMEMBER: this n_sigma is a CONSERVATIVE LOWER BOUND because")
    print(f"  the two posteriors share BAO+CMB+lensing (positively correlated),")
    print(f"  so the true variance of (mu_A - mu_B) is smaller than C_A + C_B,")
    print(f"  and the true tension is at least this large, often larger.")

    return dict(
        pair=(name_a, name_b),
        d=d, C=C, chi2=chi2_val, p_value=p_value, n_sigma=n_sigma,
    )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    banner("DESI DR2 SNe inter-sample (w0, wa) tension", char="#")
    print("Lower-bound tension between the three SNe sample posteriors,")
    print(f"computed from the cobaya chains under {CHAINS_ROOT}.")

    # --- Load all three samples and cache (mean, cov) ----------------------
    moments = {}
    for name, cfg in SAMPLES.items():
        banner(f"LOADING: {name}", char="=")
        sample_dir = CHAINS_ROOT / cfg["dir"]
        print(f"  source dir : {sample_dir}")
        s = load_combo(sample_dir, BURN_IN_FRACTION)
        mean, cov, neff = weighted_moments(s)
        vecprint("mean (w, wa)", mean)
        matprint("cov", cov)
        print(f"  N_eff = {neff:,.0f}")
        moments[name] = (mean, cov)

    # --- Pairwise tension ---------------------------------------------------
    banner("PAIRWISE TENSION", char="#")
    results = []
    for a, b in combinations(moments.keys(), 2):
        mu_a, C_a = moments[a]
        mu_b, C_b = moments[b]
        results.append(tension(a, mu_a, C_a, b, mu_b, C_b))

    # --- Summary table ------------------------------------------------------
    banner("SUMMARY (lower bounds)", char="#")
    print(f"{'pair':<28} {'chi^2':>8} {'p-value':>12} {'sigma':>8}")
    print("-" * 60)
    for r in results:
        pair = f"{r['pair'][0]:<10} vs {r['pair'][1]}"
        print(f"{pair:<28} {r['chi2']:>8.3f} {r['p_value']:>12.3e} "
              f"{r['n_sigma']:>8.2f}")
    print()
    print("Reading guide")
    print("-------------")
    print("All pairs < 1 sigma : three samples consistent. Inter-sample")
    print("                      variation in the headline 2.8/3.8/4.2 sigma")
    print("                      is statistical (different size/z-range).")
    print("Some pair >= 2 sigma : meaningful disagreement. Either")
    print("                      (a) sample-specific systematics (calibration),")
    print("                      (b) sample-specific physics signal,")
    print("                      (c) z-binning effect (each sample covers a")
    print("                          different part of the cosmic history).")
    print("                      Discriminating among (a)/(b)/(c) is the next step.")


if __name__ == "__main__":
    main()
