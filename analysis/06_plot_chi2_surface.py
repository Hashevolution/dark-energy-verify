"""
06_plot_chi2_surface.py
=======================

Three-panel visualization showing how far LambdaCDM = (-1, 0) lies
from each SNe sample's (w, wa) posterior.

Each panel:
  - 2D histogram of chain samples (posterior density, log color scale)
  - Marginal 1, 2, 3 sigma ellipses from weighted (mean, cov)
  - chain best-fit (argmin -log P)   : orange star
  - posterior mean (marginal)         : white plus
  - LCDM (-1, 0)                      : red X

Output: analysis/chi2_surface.png
"""

from __future__ import annotations

from pathlib import Path
import time

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Ellipse


REPO_ROOT = Path(__file__).resolve().parent.parent
CHAINS_ROOT = REPO_ROOT / "data" / "desi_dr2" / "chains"
OUT_PATH = REPO_ROOT / "analysis" / "chi2_surface.png"

COL_WEIGHT = 0
COL_MINUSLOGPOST = 1
COL_W = 8
COL_WA = 9

# (display name, subdir, sigma_marg from 02, DESI reported)
SAMPLES = [
    ("Pantheon+", "pantheonplus", 2.58, 2.80),
    ("Union3",    "union3",       3.38, 3.80),
    ("DES-SN5YR", "des-sn5yr",    3.94, 4.20),
]

LCDM = np.array([-1.0, 0.0])
BURN_IN = 0.30

# 2D Delta-chi^2 contour levels for n-sigma probability mass
N_SIGMA_LEVELS = [(1, 2.30), (2, 6.18), (3, 11.83)]


def load_chain(sample_dir: Path, burn_in: float) -> np.ndarray:
    parts = []
    for i in (1, 2, 3, 4):
        arr = np.loadtxt(
            sample_dir / f"chain.{i}.txt",
            comments="#",
            usecols=(COL_WEIGHT, COL_MINUSLOGPOST, COL_W, COL_WA),
        )
        n_drop = int(len(arr) * burn_in)
        parts.append(arr[n_drop:])
    return np.vstack(parts)


def weighted_moments(samples: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    w = samples[:, 0]
    x = samples[:, 2:4]
    W = w.sum()
    mean = (w[:, None] * x).sum(axis=0) / W
    dx = x - mean
    cov = (w[:, None, None] * dx[:, :, None] * dx[:, None, :]).sum(axis=0) / W
    return mean, cov


def add_ellipse(ax, mean: np.ndarray, cov: np.ndarray, dchi2: float, **kwargs):
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = eigvals.argsort()[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]
    angle = np.degrees(np.arctan2(eigvecs[1, 0], eigvecs[0, 0]))
    width = 2.0 * np.sqrt(dchi2 * eigvals[0])
    height = 2.0 * np.sqrt(dchi2 * eigvals[1])
    e = Ellipse(xy=mean, width=width, height=height, angle=angle,
                fill=False, **kwargs)
    ax.add_patch(e)
    return e


def main() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2), constrained_layout=True)

    for ax, (name, sub, sigma_marg, desi) in zip(axes, SAMPLES):
        t0 = time.time()
        samples = load_chain(CHAINS_ROOT / sub, BURN_IN)
        print(f"  {name}: loaded {len(samples):,} rows in {time.time()-t0:.1f}s")

        weights = samples[:, 0]
        mlp = samples[:, 1]
        w0 = samples[:, 2]
        wa = samples[:, 3]

        mean, cov = weighted_moments(samples)
        j_bf = int(np.argmin(mlp))
        x_bf = np.array([w0[j_bf], wa[j_bf]])

        # Plot range: chain extent extended just enough to include LCDM
        w0_lo = min(w0.min(), LCDM[0]) - 0.03
        w0_hi = max(w0.max(), LCDM[0]) + 0.03
        wa_lo = min(wa.min(), LCDM[1]) - 0.05
        wa_hi = max(wa.max(), LCDM[1]) + 0.05

        H, x_edges, y_edges = np.histogram2d(
            w0, wa, bins=90, weights=weights,
            range=[[w0_lo, w0_hi], [wa_lo, wa_hi]],
        )
        H = H.T  # shape (n_wa, n_w0) for imshow

        H_plot = np.where(H > 0, H, np.nan)
        vmax = float(np.nanmax(H_plot))
        vmin = max(float(np.nanmin(H_plot)), vmax * 1e-4)

        im = ax.imshow(
            H_plot, origin="lower", aspect="auto",
            extent=(w0_lo, w0_hi, wa_lo, wa_hi),
            cmap="viridis",
            norm=mcolors.LogNorm(vmin=vmin, vmax=vmax),
        )

        # Marginal n-sigma ellipses (white dashed)
        for n_sig, dchi2 in N_SIGMA_LEVELS:
            add_ellipse(
                ax, mean, cov, dchi2,
                ec="white", lw=1.2,
                ls="--" if n_sig < 3 else "-",
                label=f"{n_sig}{chr(963)} marginal" if n_sig == 1 else None,
            )

        # Markers: best fit, mean, LCDM
        ax.plot(*x_bf, marker="*", color="orange", ms=18,
                mec="black", mew=0.7, label="best fit", zorder=6)
        ax.plot(*mean, marker="+", color="white", ms=14, mew=2.2,
                label="posterior mean", zorder=6)
        ax.plot(*LCDM, marker="X", color="red", ms=15,
                mec="black", mew=0.7, label=r"$\Lambda$CDM", zorder=6)

        ax.set_xlabel(r"$w_0$")
        ax.set_ylabel(r"$w_a$")
        ax.set_title(f"{name}\n"
                     f"$\\sigma_{{\\rm marg}}$ = {sigma_marg:.2f}   "
                     f"DESI = {desi:.2f}")
        ax.set_xlim(w0_lo, w0_hi)
        ax.set_ylim(wa_lo, wa_hi)
        ax.legend(loc="lower left", fontsize=8, framealpha=0.85)

    fig.suptitle(
        "DESI DR2  SNe combinations: ($w_0$, $w_a$) posterior vs $\\Lambda$CDM",
        fontsize=14,
    )
    fig.savefig(OUT_PATH, dpi=150)
    print(f"\nSaved: {OUT_PATH}")


if __name__ == "__main__":
    main()
