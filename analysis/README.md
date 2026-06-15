# analysis/

Verification code. One script/notebook per question.

## Scripts

- `01_sigma_recompute.py` — From the published (w₀, wₐ) means and covariances,
  compute the Mahalanobis distance from (−1, 0) — i.e., σ — for each SNe sample.
- `02_chain_load.py` — Load the public DESI MCMC chains directly. Compute
  σ_marginal (Gaussian) and σ_empirical (chain tail, no Gaussian assumption).
- `03_sample_compare.py` — Pairwise (w₀, wₐ) tension between Pantheon+ /
  Union3 / DES-SN5YR. Conservative lower bound (shared BAO+CMB+lensing
  inflates the difference covariance).
- `04_profile_vs_marginal.py` — Test whether the ~0.2–0.4 σ gap between our
  σ_marginal and DESI's headline σ is the profile-likelihood (Δχ²_min)
  vs marginalized-posterior convention difference.
- `05_burnin_sensitivity.py` — Sweep burn-in cut over {0, 10, 20, 30, 40, 50}%
  and check whether σ_marginal moves meaningfully.
- `06_plot_chi2_surface.py` — Three-panel visualization: posterior density
  + n-σ marginal ellipses + LCDM position. Output: `chi2_surface.png`.

## Headline findings

- σ_marginal recomputed from chains (02): 2.58 / 3.38 / 3.94 vs DESI's
  2.8 / 3.8 / 4.2 → consistent ordering, residual gap of 0.2–0.4 σ.
- Pairwise SNe tension (03): all pairs < 2σ lower-bound; difference vectors
  lie along the (w₀, wₐ) degeneracy axis → samples consistent.
- Profile vs marginal (04): partially explains the gap. eig(M)/eig(C⁻¹)
  > 1 confirms non-Gaussianity; Union3 σ_profile matches DESI to ≤0.04 σ,
  but full multi-dim profile minimization (out of scope) is needed for
  a clean match on Pantheon+ / DES-SN5YR.
- Burn-in sensitivity (05): max spread 0.035 σ — burn-in is NOT the
  source of the residual gap.

## Principle

- Every result is reported alongside a robustness check:
  *Does it survive a change of normalization, metric, or data selection?*
- Exciting patterns → tighten the measurement to discriminate signal from
  artifact (self-falsification).

---

## 한국어

검증 코드. 각 스크립트는 단일 질문에 답한다.
원칙: 흥분되는 패턴은 믿지 말고 더 정밀히 쳐서 아티팩트인지 확인.

검증 결과 요약: DESI의 산수는 (우리 산수 기준) 맞고, 세 SNe 샘플은 서로
일관됨. 0.2–0.4 σ 잔차 갭의 대부분은 marginal vs profile 컨벤션 차이로
설명되며, 완전한 매치를 위해선 11차원 cobaya profile 모드가 필요함 (이
레포의 범위 밖).
