# dark-energy-verify

Independent verification of the DESI DR2 dynamical dark energy signal.

## Background

This work began from an intuition about the relativity–quantum mechanics divide
as a "perspective-dependent projection of a single reality" (monistic
relationalism). Formalization via modular theory, rainbow chains, and
observational entropy reproduced existing results across the board — a
"verified rediscovery" rather than a discovery.

The full journey is in [`notes/monistic-relationalism-note.md`](notes/monistic-relationalism-note.md);
a fast-resume summary is in [`notes/handoff-summary.md`](notes/handoff-summary.md).
Both notes are in Korean (the original working language).

The methodological pivot that led to this repo:

> Pure intuition keeps landing on existing theory.
> To get something new, start from an *observed anomaly* that existing laws
> cannot explain.

The first such target: the DESI DR2 dynamical dark energy preference at
**2.8σ–4.2σ**, depending on which supernova sample is used.

## Question under test

The signal varies across supernova samples (Pantheon+ / Union3 / DES-SN5YR).
Is that variation **physics** (a real anomaly) or **systematics** (sample-
dependent calibration)?

## Layout

- `notes/` — record of the intuition → formalization → pivot-to-anomaly arc.
- `analysis/` — verification code: σ recomputation, sample comparison,
  covariance analysis.
- `data/` — DESI public data (chains, covariance matrices).
  Large files are gitignored; see `data/README.md` for sources.

## Next steps

1. Collect (w₀, wₐ) central values, errors, and covariances for each SNe sample.
2. Recompute σ from (−1, 0) directly using the published covariances.
3. Check whether the DESI-reported 2.8–4.2σ reproduces.
4. Decompose the inter-sample variation into statistical (size, z-range) vs
   systematic (calibration procedure) components.

## References

- DESI DR2 II: [arXiv:2503.14738](https://arxiv.org/abs/2503.14738)
- DESI DR2 extended DE: [arXiv:2503.14743](https://arxiv.org/abs/2503.14743)

---

## 한국어 요약

DESI DR2가 보고한 동역학적 암흑에너지 신호(2.8σ–4.2σ)의 독립 재계산 저장소.
표본별 σ 차이가 **물리(진짜 변칙)** 인가 **계통오차(보정 차이)** 인가를 가른다.

배경 여정 전체는 `notes/monistic-relationalism-note.md` (한국어 원본),
재개용 요약은 `notes/handoff-summary.md` 참조.
