# analysis/

Verification code. One script/notebook per question.

## Plan

- `01_sigma_recompute.py` — From the published (w₀, wₐ) means and covariances,
  compute the Mahalanobis distance from (−1, 0) — i.e., σ — for each SNe sample.
- `02_chain_load.py` — Load the public DESI MCMC chains directly (Path B).
- `03_sample_compare.py` — Decompose Pantheon+ / Union3 / DES-SN5YR differences
  into statistical (sample size, z-range) vs systematic (calibration) effects.

## Principle

- Every result is reported alongside a robustness check:
  *Does it survive a change of normalization, metric, or data selection?*
- Exciting patterns → tighten the measurement to discriminate signal from
  artifact (self-falsification).

---

## 한국어

검증 코드. 각 스크립트는 단일 질문에 답한다.
원칙: 흥분되는 패턴은 믿지 말고 더 정밀히 쳐서 아티팩트인지 확인.
