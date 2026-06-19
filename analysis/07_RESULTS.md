# C′ 결과 — 표본 간 변이 분해: 지배적 통계/lever-arm + sub-2σ 비통계 잔차 2건

> 실행: `analysis/07_variation_decompose.py`, `07b_decompose_selffalsify.py` (2026-06-19)
> 입력: 01의 공개 (w₀,wₐ) 요약통계(placeholder ρ=−0.87) + 표본 메타데이터(N, z_max).
> 대상: DESI DR2 동역학 암흑에너지 신호의 표본 간 변이를 **통계(크기·z범위) vs 계통(보정)**
> 으로 분해 — `analysis/README` "next step 4"의 유일 미완.

## 세 분해

| 분해 | 질문 | 결과 |
|---|---|---|
| **A 반사실 스왑** | 2.8/3.8/4.2σ 분산을 무엇이 끄나 | 중심값 오프셋이 *더 큰* 단일 요인(스프레드 2.31 vs 0.33 오차크기 1.54), 단 둘 다 기여(비가법) |
| **B 오프셋 기하** | 중심값 차이가 lever-arm(통계)인가 직교(계통)인가 | 차이벡터 **~98% 축퇴-평행** = lever-arm. 직교 잔차 max **1.0 σ_perp**(하한) |
| **C 크기/깊이 스케일링** | 오차가 N·z_max로 설명되나 | DES σ_wa는 짧은 z_max(1.13) 추종=통계. **Union3 σ_w0는 √N 예측의 1.86배** |

## 판정

> **표본 간 변이는 지배적으로 통계/lever-arm이다** — 중심값 오프셋이 (w₀,wₐ) 축퇴선을 따라
> ~98% 정렬(B), 오차크기는 N·z_max로 추적(C). **>2σ smoking-gun 계통은 없음** → 03의
> "표본 일관(<2σ)"과 정합. 단 **sub-2σ 비통계 잔차 2건**을 정직하게 플래그:
>
> 1. **Pantheon+ vs Union3 직교 오프셋 ≥1σ_perp** (하한 — sig_perp이 C_A+C_B라 차이분산
>    과대평가, 실제는 더 클 수 있음). 한 쌍에 집중. marginal, 2σ 미만.
> 2. **Union3 오차 팽창** — 최대 N(2087)인데도 σ_w0가 √N 예측의 1.86배 → 표본크기 아닌
>    *프레임워크*(UNITY Bayesian, 더 많은 nuisance 주변화)에서 온 추가 오차.

## 자가반증 (§9.15) — 모든 플래그 강건

| 검사 | 결과 |
|---|---|
| **T1 ρ 스캔** [−0.95,−0.60] | 직교 잔차 0.96–1.28(전부 sub-2σ), 항상 Pan–Uni | **B는 ρ 아티팩트 아님** |
| **T4 평행분율** | 전 ρ서 ≥0.985 | lever-arm 주장 강건 |
| **T2 driver(A)** | 전 ρ서 중심값이 더 큰 요인(2.25–2.50 vs 1.54–1.64) | 강건 |
| **T3 메타데이터(C)** | Union3 비율 1.71–1.99(N±15%) | 오차 팽창 강건 |

→ ρ placeholder·표본수 불확실에 결론이 의존하지 않음.

## 한계 (정직)
- (w₀,wₐ) 요약·ρ는 01의 placeholder. 정확값은 DESI 부록/체인에서 검증 필요(이 컨테이너에
  체인 없음). 단 자가반증이 ρ·N 민감도를 이미 닫음.
- "직교=계통 / 평행=통계"는 *판별 보조선*이지 증명이 아님. 평행 오프셋에는 보정차이도
  섞일 수 있으나 통계와 *분리 불가*(축퇴 안). 분리되는 건 직교 성분뿐 → 그게 sub-2σ.
- Union3 팽창의 "프레임워크 기원"은 해석. 확정엔 UNITY vs SALT2 재적합 필요(범위 밖).

## 데이터 트랙 종합 (01–07)
- 01–02: σ 재계산 2.58/3.38/3.94 ≈ DESI 2.8/3.8/4.2 (순서·크기 일치).
- 03: 표본 쌍 텐션 <2σ 하한 = 일관.
- 04–05: 잔차 갭 = marginal vs profile 컨벤션(번인 아님).
- **07: 변이 분해 = 지배적 통계/lever-arm + sub-2σ 비통계 잔차 2건.**
→ **데이터 트랙(과제 C/C′) 마감.** 신호는 (DESI 산수 기준) 실재하고 표본은 일관하며,
  표본 간 변이는 정량적으로 분해됨. de Sitter 동역학 표적은 실재 = 과제 A가 겨냥할 표적 확보.

---

## English summary

C′ decomposes the DESI DR2 inter-sample variation (the headline 2.8/3.8/4.2 σ)
into statistical vs systematic parts, from public summaries (no chains needed).

(A) Counterfactual swap: central-value offsets are the larger single driver of the
σ spread, though error sizes also contribute (non-additively). (B) The pairwise
central-value differences are ~98% aligned with the (w₀,wₐ) degeneracy axis
(lever-arm / statistical); the orthogonal residual maxes at ~1 σ_perp (a lower
bound), dominated by Pantheon+ vs Union3. (C) Error sizes track N and z_max —
except Union3, whose σ_w0 is ~1.9× its √N expectation despite the largest sample,
pointing to its UNITY-Bayesian framework rather than size.

Verdict: the variation is dominantly statistical/lever-arm, with two robust but
sub-2σ non-statistical residuals (a ≥1σ orthogonal Pantheon+/Union3 offset; Union3's
inflated error budget). No >2σ smoking-gun calibration systematic — consistent with
03's <2σ. Self-falsification (07b) shows none of this hinges on the placeholder ρ
or the exact sample counts. This closes the data track: the de Sitter dynamical-w
signal is real (by DESI's own arithmetic) and the samples are consistent, so Task A
has a real target.
