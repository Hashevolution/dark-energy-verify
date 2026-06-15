"""
05_burnin_sensitivity.py
========================

Robustness check: how much does the burn-in cut move sigma_marginal?

If the spread is small (<~0.05 sigma), burn-in is ruled out as a
source of the ~0.2-0.4 sigma gap between our recomputation (02) and
the DESI-reported numbers. If the spread is large (>~0.15 sigma), the
gap could be a burn-in convention mismatch.

Method
------
Load each chain once at burn_in = 0. For each burn-in fraction in
{0.00, 0.10, 0.20, 0.30, 0.40, 0.50} re-slice and recompute
sigma_marginal from the weighted (mean, cov) of (w, wa).

USAGE
-----
    python analysis/05_burnin_sensitivity.py
"""

from __future__ import annotations

from pathlib import Path
import time

import numpy as np
from scipy.stats import chi2 as chi2_dist
from scipy.special import erfcinv


REPO_ROOT = Path(__file__).resolve().parent.parent
CHAINS_ROOT = REPO_ROOT / "data" / "desi_dr2" / "chains"

COL_WEIGHT = 0
COL_W = 8
COL_WA = 9

SAMPLES = {
    "Pantheon+": dict(dir="pantheonplus", desi_reported=2.8),
    "Union3":    dict(dir="union3",       desi_reported=3.8),
    "DES-SN5YR": dict(dir="des-sn5yr",    desi_reported=4.2),
}

LCDM = np.array([-1.0, 0.0])
BURN_INS = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50]


def banner(text: str, char: str = "=") -> None:
    print(); print(char * 72); print(text); print(char * 72)


def load_chain_full(sample_dir: Path) -> list[np.ndarray]:
    """Load all 4 chains at burn_in=0. Returns list of per-chain arrays."""
    chains = []
    for i in (1, 2, 3, 4):
        p = sample_dir / f"chain.{i}.txt"
        t0 = time.time()
        arr = np.loadtxt(p, comments="#", usecols=(COL_WEIGHT, COL_W, COL_WA))
        chains.append(arr)
        print(f"    {p.name:14s}  rows={len(arr):6d}  ({time.time()-t0:.2f}s)")
    return chains


def stack_with_burnin(chains: list[np.ndarray], burn_in: float) -> np.ndarray:
    """Drop the first burn_in fraction of each chain, concatenate."""
    parts = []
    for arr in chains:
        n_drop = int(len(arr) * burn_in)
        parts.append(arr[n_drop:])
    return np.vstack(parts)


def sigma_marg(samples: np.ndarray) -> tuple[float, float, np.ndarray, np.ndarray]:
    w = samples[:, 0]
    x = samples[:, 1:3]
    W = w.sum()
    mean = (w[:, None] * x).sum(axis=0) / W
    dx = x - mean
    cov = (w[:, None, None] * dx[:, :, None] * dx[:, None, :]).sum(axis=0) / W
    d = LCDM - mean
    Cinv = np.linalg.inv(cov)
    chi2_val = float(d @ Cinv @ d)
    p = float(chi2_dist.sf(chi2_val, df=2))
    sigma = float(np.sqrt(2) * erfcinv(p)) if p > 0 else float("inf")
    return sigma, chi2_val, mean, cov


def process_sample(name: str, cfg: dict) -> dict:
    banner(f"SAMPLE: {name}", char="=")
    print("Loading raw chains (burn_in=0):")
    chains = load_chain_full(CHAINS_ROOT / cfg["dir"])
    total_raw = sum(len(c) for c in chains)
    print(f"  total raw rows: {total_raw:,}")
    print()

    print(f"  {'burn_in':>8}  {'kept rows':>10}  {'mean_w':>9}  {'mean_wa':>9}  "
          f"{'sig_w':>8}  {'sig_wa':>8}  {'rho':>7}  {'chi^2':>8}  {'sigma':>7}")
    print("  " + "-" * 86)
    row_results = []
    for b in BURN_INS:
        samples = stack_with_burnin(chains, b)
        sigma, chi2_val, mean, cov = sigma_marg(samples)
        sig_w = np.sqrt(cov[0, 0])
        sig_wa = np.sqrt(cov[1, 1])
        rho = cov[0, 1] / (sig_w * sig_wa)
        print(f"  {b:>8.2f}  {len(samples):>10,}  "
              f"{mean[0]:>+9.4f}  {mean[1]:>+9.4f}  "
              f"{sig_w:>8.4f}  {sig_wa:>8.4f}  {rho:>+7.4f}  "
              f"{chi2_val:>8.3f}  {sigma:>7.3f}")
        row_results.append((b, sigma))
    print()
    sigmas = np.array([s for _, s in row_results])
    spread = float(sigmas.max() - sigmas.min())
    print(f"  spread (max sigma - min sigma) = {spread:.4f}")
    print(f"  DESI reports                   = {cfg['desi_reported']:.2f}")
    print(f"  sigma_marg at burn_in=0.30     = {sigmas[BURN_INS.index(0.30)]:.3f}")
    print(f"  gap to DESI at 30% burn-in     = "
          f"{sigmas[BURN_INS.index(0.30)] - cfg['desi_reported']:+.3f}")
    if spread < 0.05:
        verdict = "TIGHT - burn-in not the gap source"
    elif spread < 0.15:
        verdict = "MILD sensitivity - burn-in is a small contributor at most"
    else:
        verdict = "STRONG sensitivity - burn-in plausibly explains the gap"
    print(f"  verdict                        = {verdict}")
    return dict(name=name, sigmas=sigmas, spread=spread,
                desi=cfg["desi_reported"])


def main() -> None:
    banner("DESI DR2: burn-in sensitivity of sigma_marginal", char="#")
    print(f"Sweep burn-in fraction in {BURN_INS}")
    print("Question: is the 0.2-0.4 sigma gap (DESI - ours) sensitive to")
    print("          where we cut burn-in?")

    results = []
    for name, cfg in SAMPLES.items():
        results.append(process_sample(name, cfg))

    banner("FINAL SUMMARY", char="#")
    header = "  burn_in  " + "  ".join(f"{r['name']:>10}" for r in results)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for k, b in enumerate(BURN_INS):
        row = f"  {b:>7.2f}  " + "  ".join(f"{r['sigmas'][k]:>10.3f}" for r in results)
        print(row)
    print("  " + "-" * (len(header) - 2))
    spread_row = "  spread   " + "  ".join(f"{r['spread']:>10.4f}" for r in results)
    desi_row   = "  DESI     " + "  ".join(f"{r['desi']:>10.2f}" for r in results)
    print(spread_row)
    print(desi_row)
    print()
    max_spread = max(r["spread"] for r in results)
    print(f"Max spread across all samples: {max_spread:.4f} sigma")
    if max_spread < 0.05:
        print("=> Burn-in cut is NOT the source of the 0.2-0.4 sigma gap.")
        print("   Combined with 04, this leaves the multi-dim profile-")
        print("   minimization gap as the primary residual suspect.")
    elif max_spread < 0.15:
        print("=> Burn-in is at most a minor contributor to the gap.")
    else:
        print("=> Burn-in convention may explain part of the gap; check")
        print("   DESI's documented burn-in policy against ours.")


if __name__ == "__main__":
    main()
