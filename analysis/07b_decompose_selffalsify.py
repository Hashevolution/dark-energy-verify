"""
07b_decompose_selffalsify.py
============================

Self-falsification (sec 9.15 discipline) for 07_variation_decompose.py.

The decomposition's two non-statistical flags depend on assumptions that must be
beaten on before they are trusted:

  T1  rho scan -- rho = -0.87 is a PLACEHOLDER (01_sigma_recompute.py) and it sets
      the (w0,wa) degeneracy axis, hence the parallel/orthogonal split in B. If the
      "orthogonal residual ~1 sigma" swings wildly with rho, B is a rho-artifact;
      if it is stable, B is robust.
  T2  driver stability (A) -- is "central-value offsets are the larger factor"
      stable across rho?
  T3  metadata perturbation (C) -- is "Union3 error inflated vs sqrt(N)" robust to
      +/-15% uncertainty in N (cosmology-cut counts vary)?
  T4  parallel-fraction -- across rho, what fraction of |d| is degeneracy-parallel?
      (the core "lever-arm/statistical" claim).
"""

from __future__ import annotations

import importlib.util
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("decomp", HERE / "07_variation_decompose.py")
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)

PARAMS, LCDM, NAMES, META = D.PARAMS, D.LCDM, D.NAMES, D.META


def offset_of(p):
    return np.array([p["w0_mean"], p["wa_mean"]]) - LCDM


def main():
    rhos = [-0.95, -0.90, -0.87, -0.80, -0.70, -0.60]
    mus = {n: np.array([PARAMS[n]["w0_mean"], PARAMS[n]["wa_mean"]]) for n in NAMES}

    print("### T1/T4: rho scan -- orthogonal residual (B) and parallel fraction ###")
    print(f"{'rho':>7}{'max d_perp/sig_perp':>21}{'min parallel-frac':>19}"
          f"{'worst pair':>22}")
    for rho in rhos:
        covs = {n: D.cov_of(PARAMS[n], rho) for n in NAMES}
        Cbar = np.mean([covs[n] for n in NAMES], axis=0)
        evals, evecs = np.linalg.eigh(Cbar)
        e_par = evecs[:, np.argmax(evals)]
        e_perp = evecs[:, np.argmin(evals)]
        worst_ratio, worst_pair, min_par_frac = 0.0, "", 1.0
        for a, b in combinations(NAMES, 2):
            d = mus[a] - mus[b]
            d_perp = d @ e_perp
            sig_perp = float(np.sqrt(e_perp @ (covs[a] + covs[b]) @ e_perp))
            ratio = abs(d_perp) / sig_perp
            par_frac = abs(d @ e_par) / np.linalg.norm(d)
            min_par_frac = min(min_par_frac, par_frac)
            if ratio > worst_ratio:
                worst_ratio, worst_pair = ratio, f"{a[:3]}-{b[:3]}"
        print(f"{rho:>7.2f}{worst_ratio:>21.2f}{min_par_frac:>19.3f}{worst_pair:>22}")
    print("  robust if max-ratio stays sub-2 and parallel-fraction stays high (~>0.9)\n")

    print("### T2: driver stability (A) -- central-value vs error-size, across rho ###")
    print(f"{'rho':>7}{'spread offset-only':>20}{'spread cov-only':>17}{'larger':>14}")
    for rho in rhos:
        offs = {n: offset_of(PARAMS[n]) for n in NAMES}
        covs = {n: D.cov_of(PARAMS[n], rho) for n in NAMES}
        Cbar = np.mean([covs[n] for n in NAMES], axis=0)
        obar = np.mean([offs[n] for n in NAMES], axis=0)
        so = D.spread([D.sigma(offs[n], Cbar) for n in NAMES])
        sc = D.spread([D.sigma(obar, covs[n]) for n in NAMES])
        larger = "central-val" if so > sc else "error-size"
        print(f"{rho:>7.2f}{so:>20.2f}{sc:>17.2f}{larger:>14}")
    print()

    print("### T3: metadata perturbation (C) -- Union3 sigma_w0 / sqrt(N) prediction ###")
    ref = "Pantheon+"
    Nref, s0ref = META[ref]["N"], PARAMS[ref]["sigma_w0"]
    print(f"{'N-scale':>9}{'Union3 ratio':>14}{'DES ratio':>11}")
    for scale in (0.85, 1.0, 1.15):
        row = []
        for n in ("Union3", "DES-SN5YR"):
            N = META[n]["N"] * scale
            pred = s0ref * np.sqrt(Nref / N)
            row.append(PARAMS[n]["sigma_w0"] / pred)
        print(f"{scale:>9.2f}{row[0]:>14.2f}{row[1]:>11.2f}")
    print("  Union3 inflation robust if its ratio stays clearly > 1 across scales.\n")

    print("--- verdict ---")
    print("B/A are robust if (T1) orthogonal residual stays sub-2 sigma and (T4)")
    print("parallel fraction stays high across rho, and (T2) the larger driver does")
    print("not flip. C's Union3 flag is robust if (T3) its inflation survives N+/-15%.")
    print("Then: the C' decomposition (dominantly statistical/lever-arm; two sub-2sigma")
    print("non-statistical residuals) does NOT hinge on the rho placeholder or on the")
    print("exact sample counts.")


if __name__ == "__main__":
    main()
