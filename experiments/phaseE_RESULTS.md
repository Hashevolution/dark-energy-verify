# Phase E 결과 — magic × de Sitter 교차: de Sitter 손잡이는 작동, 그러나 magic 귀속은 혼동으로 탈락

> 실행: `phaseE_desitter_magic.py`, `phaseE_selffalsify.py`, `phaseE_confound_scan.py` (2026-06-19)
> 무대: Phase 2″의 두 [[5,1,3]] perfect tensor 홀로그래픽 코드(재사용).
> 곡률 부호 손잡이: pseudo-entropy(비-에르미트 전이행렬)의 bra-ket 어긋남 각도 δ.
>   δ=0 = AdS(보통 얽힘엔트로피), δ>0 = de Sitter형(복소 pseudo-entropy).

## 게이트 판정 요약

| 게이트 | 결과 | 판정 |
|---|---|---|
| **게이트 0** (dS측 안정자 자명성) | I·CZ가 δ 전 구간에서 Var(Re)~1e-32, Var(Im)~1e-35 | **PASS** — 무대 건강 |
| self-check (δ=0=보통 엔트로피) | pseudo(δ0)=ordinary, Im=0 정확 일치 | **PASS** |
| **게이트 E** (magic이 곡률 부호 넘어 효과?) | 원시 (b) → **복소-Clifford 통제군에서 (a)/INCONCLUSIVE** | **탈락(혼동)** |

---

## 1. 원시 신호 (흥분되는 자리)

깨끗해 *보이는* 영역 (0,2,4)에서, 곡률 부호를 dS로 켜자(δ↑):
- **magic(CS)이 상태의존 *허수* pseudo-넓이를 켬:** Var(Im) 0 → 6.1e-4, 정확히 **∝ δ²**.
- 이 허수 채널은 안정자(I)·실수 Clifford(CZ)에선 0 → "magic 전용 de Sitter 채널"처럼 보임.
- Var(Re)도 dS측에서 증폭(9.4e-3 → 1.2e-2).

→ "de Sitter측에서만, magic에 의해서만 켜지는 상태의존 허수 넓이, AdS 유사물 없음"
   = 노트 §1.2(2) "거울우주는 완벽, 진짜우주는 절반"의 수치적 정체 후보 = 원시 (b).

## 2. 자가반증 (§9.15) — 통과한 검사들

| 검사 | 결과 |
|---|---|
| T1 회전축 X/Y/Z | magic-only 성질 축-강건 (크기는 축의존, X 최소) |
| T2 2-Rényi pseudo | 측도 바꿔도 허수 채널 생존 |
| T3 cT 게이트 | 다른 magic 주입에도 생존 |
| T4 비-magic 큰 δ | CZ·I는 δ=1.2까지 Var(Im)~1e-34 (안 켜짐) |
| T5 분기절단 | max\|arg(λ)\|=0.42 ≪ π, 분기 근처 0 = complex-log 아티팩트 아님 |

→ 여기까지는 전부 통과. (b)로 거의 갈 뻔함.

## 3. 결정적 통제군 (T6) — 신호를 무너뜨림

**핵심 혼동변수:** CS는 *magic이면서 동시에 복소수*(i 성분), CZ는 *둘 다 아님*(실수).
허수 채널이 "magic" 때문인가 단순 "복소 진폭" 때문인가?
→ **복소수지만 magic=0인 Clifford 게이트**로 분리: S⊗S, S⊗I, I⊗S (전부 경계 M2 불변=magic 0).

| 게이트 | 종류 | Var(Re) δ=.45 | Var(Im) δ=.45 |
|---|---|---|---|
| CS | magic | 1.09e-2 | 3.4e-4 |
| S⊗S | Clifford 복소 | ~1e-32 | ~1e-34 |
| **S⊗I** | **Clifford 복소** | **4.35e-2** | **1.37e-3** |

**S⊗I(magic=0)가 CS보다 실수·허수 채널을 둘 다 *더 크게* 켬.** 허수 채널은 magic 전용이 아님.

## 4. 영역 전수조사 — 깨끗한 magic 영역은 *존재하지 않음*

`phaseE_confound_scan.py`: 모든 2·3-큐비트 영역에서, CS가 Var를 켜는 *모든* 영역마다
어떤 단일-bond 복소 Clifford 위상(S⊗I 또는 I⊗S)이 그것을 **재현하거나 초과**한다.

```
clean magic-only regions: 0
```

→ 이 최소 2-텐서 코드는 **magic과 국소 복소 위상을 분리하지 못한다.** δ=0(AdS)의 실수
   채널부터 이미 그렇다. 내부 bond에 거는 단일큐비트 위상은 (Cao et al. 기준으로) *국소*라
   넓이연산자를 자명하게 둬야 하지만, 코드가 너무 작아(두 perfect tensor의 최대 스크램블링)
   경계 2-큐비트 영역 엔트로피를 상태의존으로 만든다 = **유한크기 아티팩트.**

---

## 5. 판정

> **게이트 E = (a)/INCONCLUSIVE (혼동에 의한 탈락).**
> Phase 2의 1차 판정을 철회시킨 것과 *정확히 같은 실패 양식*(측도/통제 오류). de Sitter
> pseudo-entropy 손잡이 자체는 잘 작동하나(게이트 0·self-check 통과), 이 무대에서는 허수
> 채널을 magic 고유로 *인증할 수 없다* — 국소 복소 Clifford가 똑같이/더 크게 만든다.

### 5.1 소급 정정 — Phase 2″도 강등
> **Phase 2″의 "magic→넓이연산자 재현 성공"은 실수 Clifford(CZ) 통제군만 썼다.**
> 복소 Clifford(S⊗I/I⊗S/S⊗S)를 통제군에 넣으면 "상태의존 = magic" 추론이 깨진다
> (S⊗I가 더 크게 만듦). → Phase 2″ 결론은 **"실수-Clifford 통제군에 한해 성립"으로 약화**.
> 즉 노트의 magic 가설은 이 최소 코드에서 *입증되지 않았다* — 입증도 반증도 아닌 미결.

### 5.2 살아남은 성과 (정직)
1. **de Sitter 손잡이 인프라 구축:** Phase 2″ 스캐폴드 위에 pseudo-entropy(복소 넓이)를
   얹고 δ=0 self-check로 검증. 더 큰 코드에 그대로 재사용 가능.
2. **§9.15 규율이 또 작동:** 원시 (b)를 복소-Clifford 통제군이 잡아냄. 원 Phase 2″가
   *놓친* 통제군을 추가해 *과거 과잉판정까지* 교정.
3. **다음 단계 정밀 확정:** 단일-bond 위상이 *진짜로 제거 가능*해지는 **더 큰 HaPPY
   코드**(더 많은 perfect tensor, 깊은 벌크, 긴 RT 표면). Cao et al. 정리의 *국소성*은
   코드가 충분히 커야 충실히 실현됨.

---

## 6. 작업순서 영향

- 과제 E는 이 무대(최소 코드)에서 **닫힘(미결)**. 다음 무대 = **E′: 더 큰 홀로그래픽 코드.**
  - 안정자/실수+복소 Clifford 전 통제군에서 단일-bond 위상이 자명해지는지 먼저 확인(게이트 0′),
  - 통과 시에만 magic(CS/cT) 주입 → 실수·허수(de Sitter) 채널 재측정.
- **future-research-topics.md 갱신 필요:** E는 (a)/혼동 판정. Phase 2″ 소급 강등. 1순위는
  E′(큰 코드)로 이동하되, 큰 코드 구현은 자기완결이나 무거움 → 2순위 D(존재론)와 재저울질.

> 핵심 교훈 재확인: **통제군이 부족하면 아티팩트를 발견으로 착각한다.** 이번엔 "복소이되
> magic 아님"이라는 통제군 한 줄이 원시 (b)와 과거 Phase 2″ 판정을 동시에 뒤집었다.

---

## English summary

Phase E crossed Task B's magic→area mechanism (only ever tested on the AdS side)
with Task A's de Sitter regime, using pseudo-entropy of a non-Hermitian transition
matrix as the curvature-sign dial (δ=0 → ordinary entropy/AdS, δ>0 → complex
pseudo-entropy/de Sitter). Gate 0 and the δ=0 self-check pass: the de Sitter handle
works. The raw signal looked like (b): magic (CS) lifts a state-dependent IMAGINARY
pseudo-area (Var ∝ δ²) absent for stabilizer/real-Clifford gates and absent on the
AdS side — and it survived axis, measure, gate, and branch-cut self-falsification.

The decisive control killed it: complex-but-CLIFFORD gates (S⊗I, I⊗S; magic-free,
boundary M2 unchanged) reproduce and EXCEED the effect, in BOTH the real (AdS) and
imaginary (de Sitter) channels. A region scan finds ZERO regions where magic is
isolated. The minimal two-tensor code conflates magic with local complex phase — a
finite-size artifact, the same failure mode that retracted Phase 2's first verdict.

Verdict: GATE E = (a)/inconclusive by confound. Two honest payoffs: (1) a working,
reusable de Sitter pseudo-entropy construction; (2) a retroactive correction —
Phase 2″'s "magic→geometry reproduced" used only a real-Clifford (CZ) control; it
fails the complex-Clifford control, so the magic hypothesis is neither confirmed
nor refuted in the minimal code. Next stage E′: a larger HaPPY code where
single-bond phases are genuinely removable.
