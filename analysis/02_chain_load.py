"""
02_chain_load.py
================

Direct verification of the DESI DR2 dynamical dark energy significance,
using the *actual published MCMC chains* (not a Gaussian approximation).

For each SNe sample (Pantheon+, Union3, DES-SN5YR) we:
  1. Load the 4 cobaya chains for the base_w_wa model.
  2. Discard burn-in (default 30%).
  3. Stack samples with their integer weights.
  4. Compute the (weighted) mean and covariance of (w, wa).
  5. Compute the joint significance vs LambdaCDM = (-1, 0) two ways:
     - Gaussian:        chi2 = d^T C^{-1} d, with d = mean - (-1, 0)
     - Empirical tail:  fraction of (weight-counted) samples that lie
                        OUTSIDE the elliptical contour passing through LCDM.

The empirical method is the *strict* version: it does not assume the
posterior is 2D Gaussian. The two should agree if it nearly is, and
disagree if the posterior has heavy/asymmetric tails near LCDM.

Every intermediate step is printed.

USAGE
-----
    python analysis/02_chain_load.py
    python analysis/02_chain_load.py | more       # page-by-page

REQUIREMENTS
------------
    numpy, scipy

INPUTS
------
    data/desi_dr2/chains/{pantheonplus,union3,des-sn5yr}/chain.{1..4}.txt
"""

from __future__ import annotations

from pathlib import Path
import sys
import time

import numpy as np
from scipy.stats import chi2 as chi2_dist
from scipy.special import erfcinv


# -----------------------------------------------------------------------------
# Paths & sample registry
# -----------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
CHAINS_ROOT = REPO_ROOT / "data" / "desi_dr2" / "chains"

# Column indices in the cobaya chain.*.txt files (0-indexed).
# Header line:  weight  minuslogpost  logA  ns  theta_MC_100  ombh2  omch2  tau  w  wa  ...
COL_WEIGHT = 0
COL_MINUSLOGPOST = 1
COL_W = 8
COL_WA = 9

SAMPLES = {
    "Pantheon+": dict(dir="pantheonplus", desi_reported=2.8),
    "Union3":    dict(dir="union3",       desi_reported=3.8),
    "DES-SN5YR": dict(dir="des-sn5yr",    desi_reported=4.2),
}

LCDM = np.array([-1.0, 0.0])
BURN_IN_FRACTION = 0.30   # fraction of each chain to discard from the start


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
# Chain loading
# -----------------------------------------------------------------------------

def load_one_chain(path: Path, burn_in: float) -> np.ndarray:
    """Load a single cobaya chain file, return Nx3 array [weight, w, wa]."""
    t0 = time.time()
    # We only need 3 columns; loadtxt(usecols=...) saves a lot of memory & time.
    arr = np.loadtxt(
        path,
        comments="#",
        usecols=(COL_WEIGHT, COL_W, COL_WA),
    )
    n_total = len(arr)
    n_drop = int(n_total * burn_in)
    arr = arr[n_drop:]
    dt = time.time() - t0
    print(f"    {path.name:14s}  rows={n_total:6d}  burn-in drop={n_drop:5d}  "
          f"kept={len(arr):6d}  ({dt:.2f}s)")
    return arr


def load_combo(sample_dir: Path, burn_in: float) -> np.ndarray:
    """Load all 4 chains for one combo, concatenated. Returns Nx3."""
    parts = []
    for i in (1, 2, 3, 4):
        parts.append(load_one_chain(sample_dir / f"chain.{i}.txt", burn_in))
    return np.vstack(parts)


# -----------------------------------------------------------------------------
# Weighted statistics
# -----------------------------------------------------------------------------

def weighted_moments(samples: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """
    samples : N x 3  with columns [weight, w, wa]
    Returns mean (length 2), covariance (2x2), and effective sample size.
    """
    w = samples[:, 0]
    x = samples[:, 1:3]
    W = w.sum()
    mean = (w[:, None] * x).sum(axis=0) / W
    dx = x - mean
    cov = (w[:, None, None] * dx[:, :, None] * dx[:, None, :]).sum(axis=0) / W
    # Standard small-bias correction for weighted cov is
    #   1 / (W - (sum w^2)/W)
    # We don't apply it here because W is enormous and the correction is
    # numerically negligible; we just print N_eff for context.
    N_eff = (w.sum() ** 2) / (w ** 2).sum()
    return mean, cov, N_eff


# -----------------------------------------------------------------------------
# Significance from the Gaussian approximation
# -----------------------------------------------------------------------------

def sigma_gaussian(mean: np.ndarray, cov: np.ndarray, lcdm: np.ndarray) -> dict:
    d = mean - lcdm
    Cinv = np.linalg.inv(cov)
    chi2_val = float(d @ Cinv @ d)
    p_value = float(chi2_dist.sf(chi2_val, df=2))
    n_sigma = float(np.sqrt(2) * erfcinv(p_value))
    return dict(d=d, Cinv=Cinv, chi2=chi2_val, p_value=p_value, n_sigma=n_sigma)


# -----------------------------------------------------------------------------
# Significance from empirical tail (no Gaussian assumption)
# -----------------------------------------------------------------------------

def sigma_empirical(samples: np.ndarray,
                    mean: np.ndarray,
                    cov: np.ndarray,
                    lcdm: np.ndarray) -> dict:
    """
    For each sample compute its Mahalanobis distance from `mean` using the
    sample covariance, then count the weighted fraction with distance >= the
    distance from `mean` to `lcdm`. This is the model-free analog of the
    chi^2 tail.
    """
    w = samples[:, 0]
    x = samples[:, 1:3]
    Cinv = np.linalg.inv(cov)
    d_lcdm = lcdm - mean
    chi2_lcdm = float(d_lcdm @ Cinv @ d_lcdm)
    # Mahalanobis^2 of every sample from the posterior mean
    dx = x - mean
    m2 = np.einsum("ni,ij,nj->n", dx, Cinv, dx)
    outside = m2 >= chi2_lcdm
    W = w.sum()
    p_emp = float((w[outside]).sum() / W)
    # Convert empirical p-value to "n_sigma" using the same convention.
    # Guard against p_emp == 0 (signal stronger than chain can resolve).
    if p_emp == 0.0:
        n_sigma = float("inf")
    else:
        n_sigma = float(np.sqrt(2) * erfcinv(p_emp))
    return dict(chi2_lcdm=chi2_lcdm, p_empirical=p_emp, n_sigma=n_sigma,
                n_outside=int(outside.sum()), n_total=len(samples))


# -----------------------------------------------------------------------------
# Per-sample driver
# -----------------------------------------------------------------------------

def process_sample(name: str, cfg: dict) -> dict:
    banner(f"SAMPLE: {name}", char="=")

    sample_dir = CHAINS_ROOT / cfg["dir"]
    if not sample_dir.exists():
        print(f"  ERROR: directory not found: {sample_dir}")
        sys.exit(1)

    # --- STEP 1: load chains -----------------------------------------------
    print("STEP 1  Load 4 chains, drop burn-in")
    print(LINE)
    print(f"  source dir : {sample_dir}")
    print(f"  burn-in    : {BURN_IN_FRACTION*100:.0f}% of each chain")
    samples = load_combo(sample_dir, BURN_IN_FRACTION)
    print(f"  total kept rows : {len(samples):,}")
    print(f"  total weight    : {samples[:,0].sum():,.0f}")
    print()

    # --- STEP 2: weighted moments ------------------------------------------
    print("STEP 2  Weighted mean and covariance of (w, wa)")
    print(LINE)
    mean, cov, neff = weighted_moments(samples)
    vecprint("mean (w, wa)", mean)
    matprint("cov", cov)
    sig_w = np.sqrt(cov[0, 0])
    sig_wa = np.sqrt(cov[1, 1])
    rho = cov[0, 1] / (sig_w * sig_wa)
    print(f"  sigma_w  = {sig_w:.4f}")
    print(f"  sigma_wa = {sig_wa:.4f}")
    print(f"  rho      = {rho:+.4f}")
    print(f"  N_eff    = {neff:,.0f}   (effective sample size)")
    print()

    # --- STEP 3: Gaussian-approx significance ------------------------------
    print("STEP 3  Gaussian-approx significance from posterior moments")
    print(LINE)
    g = sigma_gaussian(mean, cov, LCDM)
    vecprint("d = mean - LCDM", g["d"])
    print(f"  chi^2     = {g['chi2']:.4f}")
    print(f"  p-value   = {g['p_value']:.4e}   (chi^2 with 2 dof)")
    print(f"  n_sigma   = {g['n_sigma']:.3f}   (sqrt(2)*erfcinv)")
    print()

    # --- STEP 4: empirical-tail significance -------------------------------
    print("STEP 4  Empirical-tail significance (no Gaussian assumption)")
    print(LINE)
    e = sigma_empirical(samples, mean, cov, LCDM)
    print(f"  Mahalanobis^2 from mean to LCDM   = {e['chi2_lcdm']:.4f}")
    print(f"  samples outside that ellipse      = {e['n_outside']:,} / {e['n_total']:,}")
    print(f"  weighted empirical p-value        = {e['p_empirical']:.4e}")
    if np.isfinite(e["n_sigma"]):
        print(f"  empirical n_sigma                 = {e['n_sigma']:.3f}")
    else:
        print(f"  empirical n_sigma                 = >>> chain-limited (p=0) <<<")
    print()

    # --- STEP 5: compare ---------------------------------------------------
    print("STEP 5  Compare with DESI-reported sigma")
    print(LINE)
    reported = cfg["desi_reported"]
    print(f"  DESI reports          : {reported:.2f} sigma")
    print(f"  Gaussian (this script): {g['n_sigma']:.2f} sigma   "
          f"(delta {g['n_sigma'] - reported:+.2f})")
    if np.isfinite(e["n_sigma"]):
        print(f"  Empirical (this script): {e['n_sigma']:.2f} sigma   "
              f"(delta {e['n_sigma'] - reported:+.2f})")
    else:
        print(f"  Empirical (this script): chain-limited (lower bound only)")

    return dict(
        name=name,
        mean=mean, cov=cov, sig_w=sig_w, sig_wa=sig_wa, rho=rho, neff=neff,
        gaussian=g, empirical=e, reported=reported,
    )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    banner("DESI DR2 dynamical DE significance - direct from MCMC chains",
           char="#")
    print("Model      : base_w_wa  (LambdaCDM + (w0, wa))")
    print("Null       : (w, wa) = (-1, 0)")
    print(f"Chains at  : {CHAINS_ROOT}")
    print("Likelihood : DESI BAO (all) + Planck NPIPE + ACT lensing + SNe")

    results = []
    for name, cfg in SAMPLES.items():
        results.append(process_sample(name, cfg))

    banner("SUMMARY", char="#")
    header = (f"{'sample':<12} {'sigma_w':>9} {'sigma_wa':>9} {'rho':>7} "
              f"{'sigma_G':>9} {'sigma_E':>9} {'DESI':>7} {'dG':>7} {'dE':>7}")
    print(header)
    print("-" * len(header))
    for r in results:
        sg = r["gaussian"]["n_sigma"]
        se = r["empirical"]["n_sigma"]
        se_str = f"{se:>9.2f}" if np.isfinite(se) else f"{'limit':>9}"
        dE = se - r["reported"] if np.isfinite(se) else float("nan")
        dE_str = f"{dE:>+7.2f}" if np.isfinite(dE) else f"{'-':>7}"
        print(f"{r['name']:<12} "
              f"{r['sig_w']:>9.4f} {r['sig_wa']:>9.4f} {r['rho']:>+7.3f} "
              f"{sg:>9.2f} {se_str} {r['reported']:>7.2f} "
              f"{sg - r['reported']:>+7.2f} {dE_str}")
    print()
    print("sigma_G = Gaussian approx (d^T C^-1 d -> chi^2_2 tail)")
    print("sigma_E = empirical tail (weighted fraction of samples outside")
    print("          the Mahalanobis ellipse passing through LCDM)")
    print("Agreement of sigma_G and sigma_E means the posterior is close")
    print("to Gaussian near LCDM; large disagreement signals non-Gaussianity.")


if __name__ == "__main__":
    main()
