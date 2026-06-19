# Phase D 결과 — §9.8 "초과분 부호변화"는 측도 아티팩트로 확정 (유일 독창 카드 닫힘)

> 실행: `phaseD_monogamy_excess.py`, `phaseD_selffalsify.py` (2026-06-19)
> 대상: 노트 §9.8 "얽힘 종류 = 독립 실재 층" — 레포의 *유일하게 살아남은 독창 카드*.
> 무대: GHZ↔W 순수 3-큐비트 족(§9.8이 곧 "GHZ/W 종류 분리"). 순수상태라 CKW가 정확 등식.

## 결판 대상

노트 §9.8의 유일 잔여 신호:
> 전역얽힘 E(폰노이만) − CKW잔차 τ_res(tangle) 초과분이 **+0.56→−0.31 부호변화**.
> monogamy 완전재현이면 일정/0이어야 → 부호변화 = 신호?
> **단, E(엔트로피) vs τ_res(tangle) 측도 불일치 아티팩트 의심. 미결.**

→ 통일 측도(tangle)로 재계산해 부호변화가 살아남나 결판.

## 결정적 결과

| 측도 구성 | 정의 | 범위 | 부호변화 |
|---|---|---|---|
| **MISMATCH** | E_vN(엔트로피) − 전체쌍 tangle | +1.000 → **−0.415** | **있음** (§9.8 재현) |
| **UNIFIED** | τ1(tangle) − 쌍 tangle = **τ3 (CKW)** | +1.000 → +0.000 | **없음** (부호확정 ≥0) |

- **MISMATCH가 §9.8 부호변화를 충실히 재현**(노트 +0.56→−0.31, 본 실험 +1.0→−0.415, 같은 양→음 단조 구조; 크기 차이는 족 차이).
- **UNIFIED = τ3 (3-tangle)은 CKW 항등식으로 정확히 ≥0** — 부호변화 불가능.
- CKW 항등식 $τ_1(A{:}BC)=C(A{:}B)^2+C(A{:}C)^2+τ_3$ 기계정밀도 성립(max 오차 1.1e-8).

→ **부호변화는 오직 "엔트로피 − tangle" 측도 불일치에만 존재.** 통일 tangle 측도에선
   잔차가 정확히 τ3≥0이라 부호확정. **노트가 의심한 측도 아티팩트, 확정.**

## 자가반증 (§9.15) — 모든 통제군 일치

| 검사 | 결과 |
|---|---|
| **T1** 전역 측도 {vN, linear, Rényi-2, Rényi-½} | 넷 다 부호변화하나 깊이가 −0.375~−0.485로 **제각각 = 비물리** |
| **T2** 잔차 측도 {C², C, 2×쌍C²} | 교차 깊이 −0.415~−1.082로 **규약 의존** |
| **T3** 다른 족(gGHZ+곱상태) | mismatch 부호변화는 **족 의존**(이 족에선 안 뒤집힘), τ3는 **항상 ≥0** |
| **T4** CKW 항등식 전 구간 | max 오차 1.1e-8 = **불변 등뼈 확인** |

→ 부호변화는 전역·잔차 측도 *둘 다*에, 그리고 *족*에까지 의존 = 규약 산물. 불변량(τ3)만이
   족·측도 무관하게 부호확정. **아티팩트 확정.**

## 판정

> **과제 D = 닫힘. §9.8 "초과분 부호변화" = 측도 아티팩트(노트의 자기 의심을 엄밀 확정).**
> "얽힘 종류 = 독립 실재 층"의 종류 분리는 **표준 CKW monogamy의 재현**일 뿐이며, 거기서
> 새 물리(초과 신호)는 나오지 않는다. τ3(3-tangle, GHZ형 잔차)는 실재하나 *이미 알려진*
> 표준량이다.

### 함의 (정직)
- 레포의 **유일하게 살아남은 독창 카드가 닫혔다.** §9.8의 차별성은 *측도 불일치가 만든
  착시*였다 — task-A-B §4가 RQD(arXiv:2412.05979)에 "포위"라 했던 그 카드가, 외부 포위
  이전에 *내부적으로도* 새 신호가 없었음이 확정.
- 이는 손실이 아니라 **지도의 완성**이다(핸드오버 §3.D: "닫아두면 차별성 소멸 → 그래서
  결판"). 결판 결과가 "아티팩트"여도, 미결 카드를 *확정적으로* 처리한 것 자체가 산출.
- 방법론 교훈 재확인: **서로 다른 측도(엔트로피 vs tangle)를 빼면 부호는 규약이 정한다.**
  불변 명제는 CKW 등식뿐. 노트가 이미 의심했고, 이제 수치로 못박음.

## 작업순서 영향
- D 닫힘 → 레포의 *이론* 트랙에서 미결 독창 카드는 **소진**. 남은 좌표:
  - **E′**(큰 홀로그래픽 코드, magic×de Sitter 재시험) — 무겁지만 자기완결,
  - **C′**(데이터: 통계 vs 계통 분해) — 독립 실행 가능.
- 이론 단독 차별 입구가 닫혔으므로, 핸드오버의 원 전략("데이터(b)에서 출발")이 재차 유효.

---

## English summary

Phase D resolves the note's sec 9.8 open card — the repo's only surviving original
differentiation ("entanglement KIND = independent reality layer"). Its single
residual signal was an "excess" E(A:BC) − τ_res that changed sign +0.56→−0.31,
with E a von Neumann ENTROPY and τ_res a CKW residual TANGLE; the note suspected a
measure mismatch but left it open.

On the GHZ↔W pure three-qubit family (sec 9.8 is literally GHZ/W kind-separation),
CKW is an exact identity τ1(A:BC)=C(A:B)²+C(A:C)²+τ3 (verified to 1e-8). Result:
the MISMATCH excess (entropy − all-pair tangle) reproduces the sign change
(+1.0→−0.415), but the UNIFIED excess (tangle − tangle = τ3) is exactly ≥0 and
never changes sign. Self-falsification confirms the crossing is convention-
dependent — it shifts with the global measure (vN/linear/Rényi), the residual
measure, and even the state family — while τ3 stays sign-definite everywhere.

Verdict: the sec 9.8 signal is a MEASURE ARTIFACT (the note's own suspicion, now
rigorous). Kind-separation reproduces standard CKW monogamy; no new physics in the
excess. The repo's last original theory card closes — completing the map rather
than losing ground. Remaining coordinates: E′ (larger holographic code) and C′
(data: statistical-vs-systematic decomposition).
