"""
04_profile_vs_marginal.py
=========================

Investigate the ~0.2-0.4 sigma gap between our marginalized-posterior
significance (from 02_chain_load.py) and the DESI-reported headline
significance.

Hypothesis under test
---------------------
DESI may quote n_sigma via a profile-likelihood / Delta-chi^2_min
convention (the 'frequentist' significance) rather than a marginalized
posterior tail. For non-Gaussian posteriors these differ: typically

    sigma_profile  >=  sigma_marginal

because marginalization integrates over directions of varying curvature
while profiling tracks the tightest one. If the gap is wholly explained
by the profile convention, sigma_profile here should match DESI.

Method
------
We compute three numbers per sample:

  (M) sigma_marginal :
        Weighted (mean, cov) of (w, wa) -> chi^2 = d^T C^-1 d at LCDM
        -> sigma from chi^2_2 tail. Same as 02.

  (P) sigma_profile :
        Bin chain in (w, wa). In each bin with enough samples take
        min(-2 log P) - chi^2_min,global  =:  chain-resolved profile
        chi^2 at the bin center. OLS-fit a 2D quadratic in (dw, dwa)
        to those bin minima. The quadratic coefficients give a
        curvature matrix M such that

            Delta_chi^2(x) ~= (x - x_bf)^T M (x - x_bf)

        near the best fit. Evaluate at LCDM -> sigma_profile.

  (S) sigma_chain_lookup :
        Sanity number only. Find the chain's 30 nearest samples to
        LCDM, take their min(-2 log P) - chi^2_min. The chain barely
        visits LCDM if it's in the tail, so this is biased UPWARD
        in -log P (and thus is a lower bound on sigma_profile when
        sampling is sparse). Useful as a "is the answer in the right
        ballpark" check, not as a measurement.

Assumptions
-----------
- Flat priors on (w, wa). Then profile -log L equals profile -log P
  up to a constant inside the (w, wa) plane.
- The minus-log-posterior column in cobaya output is column 1 of the
  chain (after the '#' header row), as for the other w, wa columns.

USAGE
-----
    python analysis/04_profile_vs_marginal.py
"""

from __future__ import annotations

from pathlib import Path
import time

import numpy as np
from scipy.stats import chi2 as chi2_dist
from scipy.special import erfcinv


# -----------------------------------------------------------------------------
# Paths & sample registry
# -----------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
CHAINS_ROOT = REPO_ROOT / "data" / "desi_dr2" / "chains"

COL_WEIGHT = 0
COL_MINUSLOGPOST = 1
COL_W = 8
COL_WA = 9

# sigma_marg values are pre-recorded from 02_chain_load.py so we can flag any
# drift between the two scripts.
SAMPLES = {
    "Pantheon+": dict(dir="pantheonplus", desi_reported=2.8, sigma_marg_02=2.577),
    "Union3":    dict(dir="union3",       desi_reported=3.8, sigma_marg_02=3.378),
    "DES-SN5YR": dict(dir="des-sn5yr",    desi_reported=4.2, sigma_marg_02=3.935),
}

LCDM = np.array([-1.0, 0.0])
BURN_IN_FRACTION = 0.30

N_BINS = 25                  # 25x25 grid over (w, wa) chain extent
MIN_SAMPLES_PER_BIN = 5      # bins below this are dropped from the surface fit
N_LOOKUP_NEIGHBORS = 30      # for the chain-direct sanity lookup near LCDM


# -----------------------------------------------------------------------------
# Pretty-print helpers
# -----------------------------------------------------------------------------

LINE = "-" * 72


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
# Chain loading: 4 columns (weight, -log P, w, wa)
# -----------------------------------------------------------------------------

def load_chain_full(sample_dir: Path, burn_in: float) -> np.ndarray:
    parts = []
    for i in (1, 2, 3, 4):
        p = sample_dir / f"chain.{i}.txt"
        t0 = time.time()
        arr = np.loadtxt(
            p, comments="#",
            usecols=(COL_WEIGHT, COL_MINUSLOGPOST, COL_W, COL_WA),
        )
        n_drop = int(len(arr) * burn_in)
        arr = arr[n_drop:]
        print(f"    {p.name:14s}  kept={len(arr):6d}  ({time.time()-t0:.2f}s)")
        parts.append(arr)
    return np.vstack(parts)


# -----------------------------------------------------------------------------
# Significance helpers
# -----------------------------------------------------------------------------

def sigma_from_chi2(chi2_val: float, dof: int = 2) -> tuple[float, float]:
    p = float(chi2_dist.sf(chi2_val, df=dof))
    if p <= 0.0:
        return float("inf"), 0.0
    return float(np.sqrt(2) * erfcinv(p)), p


def weighted_moments_2d(samples: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    w = samples[:, 0]
    x = samples[:, 2:4]
    W = w.sum()
    mean = (w[:, None] * x).sum(axis=0) / W
    dx = x - mean
    cov = (w[:, None, None] * dx[:, :, None] * dx[:, None, :]).sum(axis=0) / W
    return mean, cov


# -----------------------------------------------------------------------------
# Profile via quadratic fit to bin-minima
# -----------------------------------------------------------------------------

def profile_quadratic_fit(samples: np.ndarray, x_bf: np.ndarray,
                          chi2_min: float,
                          n_bins: int = N_BINS,
                          min_per_bin: int = MIN_SAMPLES_PER_BIN) -> dict:
    """Bin chain, take min(-2 log P) per bin, OLS-fit a 2D quadratic centered
    at x_bf. Returns the curvature matrix M and full coefficients."""
    w_vals = samples[:, 2]
    wa_vals = samples[:, 3]
    mlp = samples[:, 1]

    w_edges = np.linspace(w_vals.min(), w_vals.max(), n_bins + 1)
    wa_edges = np.linspace(wa_vals.min(), wa_vals.max(), n_bins + 1)

    w_idx = np.clip(np.digitize(w_vals, w_edges) - 1, 0, n_bins - 1)
    wa_idx = np.clip(np.digitize(wa_vals, wa_edges) - 1, 0, n_bins - 1)

    bin_min = np.full((n_bins, n_bins), np.inf)
    bin_count = np.zeros((n_bins, n_bins), dtype=int)
    for i, j, m in zip(w_idx, wa_idx, mlp):
        if m < bin_min[i, j]:
            bin_min[i, j] = m
        bin_count[i, j] += 1

    w_centers = 0.5 * (w_edges[:-1] + w_edges[1:])
    wa_centers = 0.5 * (wa_edges[:-1] + wa_edges[1:])

    pts_w, pts_wa, pts_dchi2 = [], [], []
    for i in range(n_bins):
        for j in range(n_bins):
            if bin_count[i, j] >= min_per_bin:
                pts_w.append(w_centers[i])
                pts_wa.append(wa_centers[j])
                pts_dchi2.append(2 * bin_min[i, j] - chi2_min)

    pts_w = np.array(pts_w)
    pts_wa = np.array(pts_wa)
    pts_dchi2 = np.array(pts_dchi2)
    n_filled = len(pts_dchi2)
    if n_filled < 10:
        raise RuntimeError(f"Only {n_filled} filled bins; need >= 10 for quadratic fit.")

    dw = pts_w - x_bf[0]
    dwa = pts_wa - x_bf[1]

    # dchi^2 = c0 + c1 dw + c2 dwa + h11 dw^2 + h12 dw dwa + h22 dwa^2
    F = np.column_stack([
        np.ones_like(dw), dw, dwa,
        dw * dw, dw * dwa, dwa * dwa,
    ])
    coefs, residuals, _, _ = np.linalg.lstsq(F, pts_dchi2, rcond=None)
    c0, c1, c2, h11, h12, h22 = coefs

    # Curvature matrix M: dchi^2 ~= (x-x_bf)^T M (x-x_bf) for the quadratic part.
    # dw^2 coef = M00, dwa^2 coef = M11, dw*dwa coef = 2*M01.
    M = np.array([
        [h11,       h12 / 2.0],
        [h12 / 2.0, h22],
    ])

    # Goodness-of-fit
    pred = F @ coefs
    ss_res = float(np.sum((pts_dchi2 - pred) ** 2))
    ss_tot = float(np.sum((pts_dchi2 - pts_dchi2.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    return dict(
        coefs=coefs, M=M, n_filled=n_filled, total_bins=n_bins * n_bins,
        r2=r2, ss_res=ss_res, ss_tot=ss_tot,
    )


def profile_chain_lookup(samples: np.ndarray, chi2_min: float,
                          k: int = N_LOOKUP_NEIGHBORS) -> dict:
    """Find k chain samples closest to LCDM (in marginal-sigma-scaled units),
    return their min Delta_chi^2 = 2 minuslogpost - chi2_min."""
    w_vals = samples[:, 2]
    wa_vals = samples[:, 3]
    mlp = samples[:, 1]

    sig_w = w_vals.std()
    sig_wa = wa_vals.std()
    d2 = ((w_vals - LCDM[0]) / sig_w) ** 2 + ((wa_vals - LCDM[1]) / sig_wa) ** 2
    idx = np.argpartition(d2, k)[:k]
    j = idx[mlp[idx].argmin()]
    return dict(
        delta_chi2=float(2 * mlp[j] - chi2_min),
        nearest_w=float(w_vals[j]),
        nearest_wa=float(wa_vals[j]),
        k=k,
    )


# -----------------------------------------------------------------------------
# Per-sample driver
# -----------------------------------------------------------------------------

def process_sample(name: str, cfg: dict) -> dict:
    banner(f"SAMPLE: {name}", char="=")
    sample_dir = CHAINS_ROOT / cfg["dir"]

    # --- STEP 1: load -------------------------------------------------------
    print("STEP 1  Load 4 chains, columns (weight, -log P, w, wa)")
    print(LINE)
    print(f"  source dir: {sample_dir}")
    samples = load_chain_full(sample_dir, BURN_IN_FRACTION)
    print(f"  total kept rows: {len(samples):,}")
    print()

    # --- STEP 2: global chi^2_min -------------------------------------------
    print("STEP 2  Global best-fit chi^2_min = 2 * min(-log P)")
    print(LINE)
    mlp = samples[:, 1]
    j_bf = int(np.argmin(mlp))
    chi2_min = float(2 * mlp[j_bf])
    x_bf = np.array([samples[j_bf, 2], samples[j_bf, 3]])
    print(f"  chi^2_min       = {chi2_min:.4f}")
    print(f"  best-fit row    = #{j_bf}")
    vecprint("  best-fit (w, wa)", x_bf)
    print()

    # --- STEP 3: marginal sigma (sanity vs 02) ------------------------------
    print("STEP 3  Marginal sigma (recompute, sanity vs 02)")
    print(LINE)
    mean, cov = weighted_moments_2d(samples)
    vecprint("mean (w, wa)", mean)
    matprint("cov", cov)
    Cinv = np.linalg.inv(cov)
    d_lcdm_mean = LCDM - mean
    chi2_marg = float(d_lcdm_mean @ Cinv @ d_lcdm_mean)
    sigma_marg, p_marg = sigma_from_chi2(chi2_marg)
    drift = sigma_marg - cfg["sigma_marg_02"]
    print(f"  chi^2_marg(LCDM)  = {chi2_marg:.4f}")
    print(f"  sigma_marginal    = {sigma_marg:.3f}   "
          f"(02 recorded {cfg['sigma_marg_02']:.3f}, drift {drift:+.3f})")
    print()

    # --- STEP 4: profile quadratic fit --------------------------------------
    print("STEP 4  Profile chi^2 surface via quadratic fit to bin-minima")
    print(LINE)
    print(f"  grid           : {N_BINS} x {N_BINS} bins over chain extent")
    print(f"  min per bin    : {MIN_SAMPLES_PER_BIN}")
    print(f"  fit form       : dchi^2 = c0 + c1 dw + c2 dwa")
    print(f"                          + h11 dw^2 + h12 dw*dwa + h22 dwa^2")
    print(f"  expanded about : best fit  (so c0, c1, c2 should be ~0)")
    print()

    prof = profile_quadratic_fit(samples, x_bf, chi2_min)
    c0, c1, c2, h11, h12, h22 = prof["coefs"]
    print(f"  filled bins used   : {prof['n_filled']} / {prof['total_bins']}")
    print(f"  R^2 of fit         : {prof['r2']:.4f}")
    print(f"  c0  (intercept)    = {c0:+.4f}   (small = chain's argmin ~ true min)")
    print(f"  c1  (linear in dw) = {c1:+.4f}   (small = chain's argmin not biased)")
    print(f"  c2  (linear in dwa)= {c2:+.4f}")
    print(f"  h11 (dw^2)         = {h11:+.4f}")
    print(f"  h12 (dw*dwa)       = {h12:+.4f}")
    print(f"  h22 (dwa^2)        = {h22:+.4f}")
    print()

    M = prof["M"]
    matprint("Profile curvature M (dchi^2 ~ (x-x_bf)^T M (x-x_bf))", M)
    matprint("Marginal C^{-1}                                       ", Cinv)
    eig_M = np.linalg.eigvalsh(M)
    eig_Cinv = np.linalg.eigvalsh(Cinv)
    print(f"  eig(M)         = [{eig_M[0]:+.3f}, {eig_M[1]:+.3f}]")
    print(f"  eig(C^-1)      = [{eig_Cinv[0]:+.3f}, {eig_Cinv[1]:+.3f}]")
    ratios = eig_M / eig_Cinv
    print(f"  eig(M)/eig(C^-1) = [{ratios[0]:.3f}, {ratios[1]:.3f}]")
    print(f"  (>1 = profile tighter than marginal; explains positive gap)")
    print()

    # --- STEP 5: evaluate at LCDM -------------------------------------------
    print("STEP 5  Evaluate profile Delta_chi^2 at LCDM")
    print(LINE)
    d_to_lcdm = LCDM - x_bf
    vecprint("LCDM - x_bf", d_to_lcdm)
    # Two evaluations: full fitted quadratic vs pure-quadratic-only
    dw_L, dwa_L = d_to_lcdm
    dchi2_fit = float(c0 + c1 * dw_L + c2 * dwa_L
                      + h11 * dw_L ** 2 + h12 * dw_L * dwa_L + h22 * dwa_L ** 2)
    dchi2_quad = float(d_to_lcdm @ M @ d_to_lcdm)
    sigma_fit, p_fit = sigma_from_chi2(dchi2_fit)
    sigma_quad, p_quad = sigma_from_chi2(dchi2_quad)
    print(f"  via full fit (incl linear): Dchi^2 = {dchi2_fit:.3f}  -> sigma = {sigma_fit:.3f}")
    print(f"  via pure quadratic M     : Dchi^2 = {dchi2_quad:.3f}  -> sigma = {sigma_quad:.3f}")
    print(f"  (marginal for comparison : Dchi^2 = {chi2_marg:.3f}  -> sigma = {sigma_marg:.3f})")
    print()

    # --- STEP 6: chain-direct lookup near LCDM ------------------------------
    print("STEP 6  Chain lookup: 30 nearest samples to LCDM, take min(-2 log P)")
    print(LINE)
    lk = profile_chain_lookup(samples, chi2_min)
    print(f"  nearest sample (w, wa) = ({lk['nearest_w']:+.4f}, {lk['nearest_wa']:+.4f})")
    print(f"  Delta_chi^2 there      = {lk['delta_chi2']:.3f}")
    sigma_lk, _ = sigma_from_chi2(lk['delta_chi2'])
    print(f"  sigma_chain_lookup     = {sigma_lk:.3f}")
    print(f"  CAVEAT: chain barely visits LCDM tail. This is a noisy")
    print(f"          chain-resolution-limited estimate, not a measurement.")
    print()

    # --- STEP 7: summary ----------------------------------------------------
    print("STEP 7  Summary for this sample")
    print(LINE)
    print(f"  DESI reports         : {cfg['desi_reported']:.2f}")
    print(f"  sigma_marginal       : {sigma_marg:.2f}    "
          f"(delta {sigma_marg - cfg['desi_reported']:+.2f})")
    print(f"  sigma_profile (fit)  : {sigma_fit:.2f}    "
          f"(delta {sigma_fit - cfg['desi_reported']:+.2f})")
    print(f"  sigma_profile (quad) : {sigma_quad:.2f}    "
          f"(delta {sigma_quad - cfg['desi_reported']:+.2f})")
    print(f"  sigma_chain_lookup   : {sigma_lk:.2f}    (sanity only)")

    return dict(
        name=name,
        sigma_marg=sigma_marg,
        sigma_prof_fit=sigma_fit,
        sigma_prof_quad=sigma_quad,
        sigma_lookup=sigma_lk,
        desi=cfg["desi_reported"],
        eig_ratio=ratios,
    )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    banner("DESI DR2: profile-vs-marginal convention check", char="#")
    print("Question: does sigma_profile match DESI's headline numbers,")
    print("          closing the ~0.2-0.4 sigma gap that sigma_marginal")
    print("          (from 02) leaves open?")

    results = []
    for name, cfg in SAMPLES.items():
        results.append(process_sample(name, cfg))

    banner("FINAL SUMMARY", char="#")
    header = (f"{'sample':<12} {'DESI':>6} {'sM':>6} {'sP_fit':>8} {'sP_quad':>9} "
              f"{'gap_M':>7} {'gap_P':>7} {'eig_ratio':>14}")
    print(header)
    print("-" * len(header))
    for r in results:
        eig_str = f"[{r['eig_ratio'][0]:.2f}, {r['eig_ratio'][1]:.2f}]"
        print(f"{r['name']:<12} {r['desi']:>6.2f} {r['sigma_marg']:>6.2f} "
              f"{r['sigma_prof_fit']:>8.2f} {r['sigma_prof_quad']:>9.2f} "
              f"{r['sigma_marg'] - r['desi']:>+7.2f} "
              f"{r['sigma_prof_fit'] - r['desi']:>+7.2f} "
              f"{eig_str:>14}")
    print()
    print("Reading guide")
    print("-------------")
    print("If gap_P is close to 0 across all samples, profile is DESI's")
    print("convention and the gap_M (~-0.2 to -0.4) is explained.")
    print("If gap_P is still significantly negative, the gap is NOT a")
    print("profile-vs-marginal issue, and the next suspects are:")
    print("  - burn-in cut (try 20%, 40%, 50%);")
    print("  - prior boundary effects;")
    print("  - DESI using a full multi-dim minimizer (not just the (w,wa)")
    print("    plane) where extra parameters move further from their")
    print("    posterior peaks under the LCDM constraint;")
    print("  - chains we downloaded being a slightly different combo than")
    print("    the one quoted in Table 3.")
    print("eig_ratio (eig M / eig C^-1) > 1 means profile curvature is")
    print("tighter than marginal in that direction = non-Gaussian posterior.")


if __name__ == "__main__":
    main()
