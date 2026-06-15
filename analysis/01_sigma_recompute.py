"""
01_sigma_recompute.py
=====================

Recompute the "n-sigma preference for dynamical dark energy" reported by
DESI DR2 (arXiv:2503.14738), starting from the published (w0, wa) means
and covariances for three supernova samples:

    Pantheon+   ~ 2.8 sigma  (DESI report)
    Union3      ~ 3.8 sigma
    DES-SN5YR   ~ 4.2 sigma

Method (joint 2D significance, the same convention DESI uses):

    d        = (w0 - (-1), wa - 0)                # offset from LambdaCDM
    chi2     = d^T C^{-1} d                        # Mahalanobis distance squared
    p_value  = 1 - F_{chi2, dof=2}(chi2)           # tail prob under chi2_2
    n_sigma  = sqrt(2) * erfcinv(p_value)          # convert to 1D normal "sigma"

The script prints every intermediate quantity so the calculation can be
followed by eye.

USAGE
-----
    python analysis/01_sigma_recompute.py

REQUIREMENTS
------------
    numpy, scipy

IMPORTANT - VERIFY NUMBERS BEFORE TRUSTING OUTPUT
-------------------------------------------------
The values in PARAMETERS_TO_VERIFY are best-recollection approximations of
the DESI DR2 published constraints. You MUST cross-check against:
  - arXiv:2503.14738 Table 3 / Table 4 (DR2 BAO + CMB + SNe combinations)
  - The official DESI public release tables on https://data.desi.lbl.gov/
before reporting any result. Each entry has a `source` field for traceability.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import chi2 as chi2_dist
from scipy.special import erfcinv


# -----------------------------------------------------------------------------
# PARAMETERS_TO_VERIFY: cross-check against arXiv:2503.14738 before trusting
# -----------------------------------------------------------------------------
#
# For each sample we need:
#   w0_mean, wa_mean, sigma_w0, sigma_wa, rho   (correlation coefficient)
#
# The DESI DR2 paper reports asymmetric errors on wa. We symmetrize by taking
# the average of (+) and (-) errors as a first pass. The correlation rho
# between w0 and wa in the (w0, wa) parametrization is strongly negative
# (typically rho ~ -0.85 to -0.9); the exact value comes from the published
# covariance matrix or MCMC chain. Treat these as PLACEHOLDERS.
#
PARAMETERS_TO_VERIFY = {
    "Pantheon+": dict(
        w0_mean=-0.838,
        wa_mean=-0.62,
        sigma_w0=0.055,
        sigma_wa=0.205,        # avg of +0.22, -0.19
        rho=-0.87,             # PLACEHOLDER - get from chain or appendix
        source="arXiv:2503.14738 - VERIFY exact values from Table 3",
    ),
    "Union3": dict(
        w0_mean=-0.667,
        wa_mean=-1.09,
        sigma_w0=0.088,
        sigma_wa=0.29,         # avg of +0.31, -0.27
        rho=-0.87,             # PLACEHOLDER
        source="arXiv:2503.14738 - VERIFY exact values from Table 3",
    ),
    "DES-SN5YR": dict(
        w0_mean=-0.752,
        wa_mean=-0.86,
        sigma_w0=0.057,
        sigma_wa=0.21,         # avg of +0.22, -0.20
        rho=-0.87,             # PLACEHOLDER
        source="arXiv:2503.14738 - VERIFY exact values from Table 3",
    ),
}

# DESI-reported sigma for each sample, for direct comparison.
DESI_REPORTED_SIGMA = {
    "Pantheon+": 2.8,
    "Union3":    3.8,
    "DES-SN5YR": 4.2,
}

# The null hypothesis we are measuring distance from.
LCDM = np.array([-1.0, 0.0])   # (w0, wa) for cosmological constant


# -----------------------------------------------------------------------------
# Pretty-print helpers
# -----------------------------------------------------------------------------

LINE = "-" * 72
DLINE = "=" * 72


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


# -----------------------------------------------------------------------------
# Core: one-sample sigma calculation, fully traced
# -----------------------------------------------------------------------------

def recompute_sigma(name: str, p: dict, lcdm: np.ndarray) -> dict:
    """Compute n-sigma preference for one sample, printing every step."""

    banner(f"SAMPLE: {name}", char="=")
    print(f"  source : {p['source']}")
    print()

    # --- STEP 1: published inputs -------------------------------------------
    print("STEP 1  Published inputs (means, marginal errors, correlation)")
    print(LINE)
    print(f"  w0_mean   = {p['w0_mean']:+.4f}")
    print(f"  wa_mean   = {p['wa_mean']:+.4f}")
    print(f"  sigma_w0  = {p['sigma_w0']:.4f}")
    print(f"  sigma_wa  = {p['sigma_wa']:.4f}")
    print(f"  rho       = {p['rho']:+.3f}   (correlation between w0, wa)")
    print()

    # --- STEP 2: build covariance matrix ------------------------------------
    print("STEP 2  Build 2x2 covariance matrix C")
    print(LINE)
    print("  C[0,0] = sigma_w0^2")
    print("  C[1,1] = sigma_wa^2")
    print("  C[0,1] = C[1,0] = rho * sigma_w0 * sigma_wa")
    print()
    C = np.array([
        [p["sigma_w0"]**2,                       p["rho"]*p["sigma_w0"]*p["sigma_wa"]],
        [p["rho"]*p["sigma_w0"]*p["sigma_wa"],   p["sigma_wa"]**2],
    ])
    matprint("C", C)
    detC = np.linalg.det(C)
    print(f"  det(C) = {detC:.6e}   (must be > 0 for valid covariance)")
    eigs = np.linalg.eigvalsh(C)
    vecprint("eig(C)", eigs)
    print(f"  cond(C) = {eigs.max()/eigs.min():.2f}   (large = elongated, expect ~50+ here)")
    print()

    # --- STEP 3: invert covariance ------------------------------------------
    print("STEP 3  Invert covariance")
    print(LINE)
    Cinv = np.linalg.inv(C)
    matprint("C^{-1}", Cinv)
    # Sanity: C * Cinv should be identity
    I_check = C @ Cinv
    print("  sanity: C @ C^{-1} should be identity")
    matprint("C @ C^{-1}", I_check, fmt="{:+.3e}")
    print()

    # --- STEP 4: offset from LCDM -------------------------------------------
    print("STEP 4  Offset vector d = mean - LCDM")
    print(LINE)
    mean = np.array([p["w0_mean"], p["wa_mean"]])
    vecprint("mean", mean)
    vecprint("LCDM", lcdm)
    d = mean - lcdm
    vecprint("d = mean - LCDM", d)
    print(f"  d[0] = w0_mean - (-1) = {d[0]:+.4f}   (>0 means w0 > -1, less negative)")
    print(f"  d[1] = wa_mean -   0  = {d[1]:+.4f}   (<0 means wa < 0, evolving)")
    print()

    # --- STEP 5: chi^2 = d^T C^{-1} d ---------------------------------------
    print("STEP 5  chi^2 = d^T C^{-1} d   (Mahalanobis distance squared)")
    print(LINE)
    Cinv_d = Cinv @ d
    vecprint("C^{-1} d", Cinv_d)
    chi2_val = float(d @ Cinv_d)
    # Manual expansion for inspection
    a = Cinv[0,0]*d[0]**2
    b = 2*Cinv[0,1]*d[0]*d[1]
    c = Cinv[1,1]*d[1]**2
    print(f"  term1: C^{{-1}}[0,0] * d[0]^2          = {a:+.4f}")
    print(f"  term2: 2 * C^{{-1}}[0,1] * d[0]*d[1]   = {b:+.4f}")
    print(f"  term3: C^{{-1}}[1,1] * d[1]^2          = {c:+.4f}")
    print(f"  sum                                    = {a+b+c:+.4f}")
    print(f"  d @ C^{{-1}} @ d (matrix form)         = {chi2_val:+.4f}")
    print()

    # --- STEP 6: chi^2 -> p-value (2 dof) -----------------------------------
    print("STEP 6  Convert chi^2 to p-value under chi^2 with 2 dof")
    print(LINE)
    p_value = float(chi2_dist.sf(chi2_val, df=2))
    print("  p_value = P(chi2_{dof=2} > chi2_val)")
    print(f"          = scipy.stats.chi2.sf({chi2_val:.4f}, df=2)")
    print(f"          = {p_value:.6e}")
    print()

    # --- STEP 7: p-value -> 1D-equivalent sigma -----------------------------
    print("STEP 7  Convert p-value to 1D-Gaussian equivalent n_sigma")
    print(LINE)
    print("  n_sigma = sqrt(2) * erfcinv(p_value)")
    print("  (this is the convention DESI uses: 'equivalent significance')")
    n_sigma = float(np.sqrt(2) * erfcinv(p_value))
    print(f"          = sqrt(2) * erfcinv({p_value:.4e})")
    print(f"          = {n_sigma:.3f}")
    print()

    # --- STEP 8: comparison to DESI-reported --------------------------------
    print("STEP 8  Compare to DESI-reported sigma")
    print(LINE)
    reported = DESI_REPORTED_SIGMA[name]
    delta = n_sigma - reported
    print(f"  recomputed : {n_sigma:.2f} sigma")
    print(f"  DESI says  : {reported:.2f} sigma")
    print(f"  difference : {delta:+.2f} sigma  "
          f"({'MATCH' if abs(delta) < 0.3 else 'MISMATCH - check inputs (esp. rho)'})")

    return dict(
        name=name,
        chi2=chi2_val,
        p_value=p_value,
        n_sigma=n_sigma,
        desi_reported=reported,
        delta=delta,
    )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    banner("DESI DR2 dynamical DE significance - independent recomputation",
           char="#")
    print("Null hypothesis: LambdaCDM, i.e. (w0, wa) = (-1, 0)")
    print()
    print("WARNING: the values in PARAMETERS_TO_VERIFY are placeholders.")
    print("         Cross-check against arXiv:2503.14738 Table 3 before trusting.")

    results = []
    for name, p in PARAMETERS_TO_VERIFY.items():
        results.append(recompute_sigma(name, p, LCDM))

    # --- summary table ------------------------------------------------------
    banner("SUMMARY", char="#")
    header = f"{'sample':<12} {'chi^2':>8} {'p-value':>12} {'sigma (mine)':>14} {'sigma (DESI)':>14} {'delta':>8}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r['name']:<12} "
              f"{r['chi2']:>8.3f} "
              f"{r['p_value']:>12.3e} "
              f"{r['n_sigma']:>14.2f} "
              f"{r['desi_reported']:>14.2f} "
              f"{r['delta']:>+8.2f}")
    print()
    print("Reading: a 'delta' near 0 (|delta| < 0.3) means our recomputation")
    print("reproduces the DESI-reported significance, given the assumed inputs.")
    print("Large |delta| means one of (means, sigmas, rho) needs correction -")
    print("the most likely culprit is rho (correlation), since means and")
    print("marginal errors are quoted directly while rho must be inferred.")


if __name__ == "__main__":
    main()
