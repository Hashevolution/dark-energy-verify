# DESI DR2 chain sources

All downloaded 2026-06-15 from the public DESI DR2 cosmology release
(October 6, 2025): https://www.desi.lbl.gov/2025/10/06/desi-dr2-cosmology-chains-and-data-products-released/

Paper: arXiv:2503.14738 (DESI DR2 Results II).

## Cobaya MCMC chains (`chains/`)

Model: `base_w_wa` (LambdaCDM + w0, wa). Likelihood: DESI BAO (all) + Planck
2018 low-l TT + low-l EE + Planck NPIPE high-l CamSpec TTTEEE + ACT DR6
lensing + each SNe sample.

Base URL:
  https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/cobaya/base_w_wa/

Subdirectories (each holds 4 chains + .covmat + .input.yaml + .updated.yaml):

- `pantheonplus/` from
  `desi-bao-all_pantheonplus_planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_planck-NPIPE-highl-CamSpec-TTTEEE_planck-act-dr6-lensing/`
- `union3/` from
  `desi-bao-all_union3_planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_planck-NPIPE-highl-CamSpec-TTTEEE_planck-act-dr6-lensing/`
- `des-sn5yr/` from
  `desi-bao-all_desy5sn_planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_planck-NPIPE-highl-CamSpec-TTTEEE_planck-act-dr6-lensing/`

## Download commands

See `analysis/download_chains.sh` or the curl loop in this repo.
