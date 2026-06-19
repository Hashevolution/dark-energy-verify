# Phase E′ 결과 — 더 큰 코드도 혼동 못 풂(구조적). Var(S) 진단법 자체가 부적합으로 판명

> 실행: `phaseEprime_3tensor.py`, `phaseEprime_scan.py`, `phaseEprime_verify.py` (2026-06-19)
> 무대: 3개 [[5,1,3]] perfect tensor 선형 코드 T1–T2–T3(인접쌍당 2 bond). 경계 7큐비트.
> 목표: Phase E의 혼동(단일-bond 복소 Clifford가 magic처럼 넓이를 상태의존化)이
> *더 큰 코드*에서 해소되는지(=유한크기 아티팩트였는지) 직접 시험.

## 게이트 진행

| 단계 | 결과 |
|---|---|
| 게이트 0′ (region A=T1.(0,1,2)) | 모든 게이트 Var~0 — **2-bond 컷 포화**(S_A=2ln2), 상태의존 여지 없음 |
| 영역 스캔(4-게이트 통제) | 깨끗해 *보이는* 영역 몇 개 출현(G1:1, G2:2, 양쪽:5) → 원시 "혼동 해소?" |
| **전수 검증(64 대각 게이트)** | **모든 후보 혼동.** magic-free 32개 중 최대 Var=0.079 ≫ magic 최소 Var=0.0018 |

## 핵심 결과

**스캔의 "깨끗한" 영역은 빈약한 통제군(4개)의 착시였다.**
CS와 같은 구조인 **대각 2-큐비트 게이트 전수**(diag(1,iᵃ,iᵇ,iᶜ), 64개; 32개가 magic-free
Clifford)로 후보 영역을 검증하니:

| 후보 영역 | 무대 | max Var(magic-free) | min Var(magic) | 판정 |
|---|---|---|---|---|
| (2,4) | G1 | **3.75e-2** | 1.76e-3 | 혼동 |
| (1,2,5) | G2 | **7.91e-2** | 3.08e-3 | 혼동 |
| (0,3,4,6) | G2 | **7.91e-2** | 3.08e-3 | 혼동 |
| (0,2,5) | 양쪽 | **3.75e-2** | 4.48e-3 | 혼동 |
| (1,3,4,6) | 양쪽 | **3.75e-2** | 4.48e-3 | 혼동 |

→ **magic-free Clifford 위상이 magic보다 *더 큰* 상태의존성을 만든다.** Phase E(2-텐서)와
   동일. **3-텐서 = 깨끗한 영역 0개 = 개선 없음.** 혼동은 코드 크기에 무관 = **구조적.**

## 판정

> **과제 E′ = 더 큰 코드(3-텐서)도 혼동을 풀지 못함. 혼동은 구조적이며, "코드를 키운다"가
> 해법이 아니다.** 2→3 텐서로 가도 전수 통제군에서 깨끗한 영역은 여전히 0.

### 메타-교훈 (가장 중요) — 같은 실패가 한 단계 위에서 재발
- Phase E가 Phase 2″를 무너뜨린 방식(부족한 통제군 → 복소 Clifford 통제군이 신호 사살)이
  **이번엔 내 자신의 스캔에서 재발**: 4-게이트 통제로 "깨끗한 영역"을 봤으나, 전수 통제군이
  전부 죽임. **§9.15 규율이 또, 이번엔 내 중간결과에 작동.**
- 함의: **Var(S_A)-over-bulk-states 진단법 자체가 magic→기하 효과의 부적합한 도구다.**
  국소 복소 Clifford 위상이 sub-maximal 영역 엔트로피를 일반적으로 상태의존化하므로,
  이 프록시는 magic을 *원리적으로* 분리하지 못한다 — 2든 3든 텐서 수와 무관.

### 다음 방향 정정 (정직)
- ❌ "더 큰 HaPPY 코드"는 해법이 아님(2→3에서 혼동 안 줄음, 큰 코드는 지수비용으로 무의미).
- ✅ 올바른 도구 = **Var(S) 프록시가 아니라 비국소 magic을 *연산자 수준*에서 직접 계산**
  (Cao et al.의 실제 측도: 분할면 가로지르는 비안정자성 중 국소 유니터리로 못 없애는 부분).
  이는 넓이연산자 스펙트럼/모듈러 해밀토니안 추출을 요하며, 현재 스캐폴드 너머 = **추적/외부
  검증 대기**로 강등.

## 작업순서 영향
- E′(큰 코드) **닫힘 — 부정적**. magic 가설은 *tractable 정밀 시뮬레이션으로는 입증 불가*가
  확정. (반증도 아님 — 도구가 부적합한 것이지 가설이 틀린 게 아님.)
- de Sitter 확장(pseudo-entropy)은 AdS측 혼동에 이미 막혀 실행 불가(같은 프록시 사용) → 보류.
- **세션의 모든 *능동* 좌표 소진.** 남은 건 전부 외부 검증/문헌 정독 대기(Cao et al. 비국소
  magic 직접계산, cobaya profile, de Sitter EE 최전선).

---

## English summary

Phase E′ built a 3-perfect-tensor code to test whether Phase E's confound (a
single-bond complex-Clifford phase faking the magic→state-dependent-area effect)
was a finite-size artifact that a larger code would fix.

Region scan with a 4-gate control set produced a few apparently-clean magic-only
regions — but verifying them against the FULL 64 diagonal 2-qubit gates (32 of
which are magic-free Clifford) shows EVERY candidate is confounded: magic-free
Clifford phases lift Var(S_R) to 0.04–0.08, far more than the magic gates' ~0.002.
The 3-tensor code yields zero genuinely clean regions — no improvement over the
2-tensor case. The confound is structural, independent of code size.

Meta-lesson: this is the SAME failure mode that Phase E used to overturn Phase 2″
(an under-powered control set faking a signal), now recurring one level up in my
own scan. The deeper implication: the Var(S_A)-over-bulk-states proxy is the wrong
diagnostic for magic→geometry — local complex-Clifford phases generically make
sub-maximal region entropies state-dependent, so the proxy cannot isolate magic at
ANY tractable code size.

Verdict: E′ closes negatively. "Bigger code" is not the fix (2→3 tensors did not
reduce the confound). The magic hypothesis is unprovable by tractable exact
simulation via this proxy; a faithful test needs the non-local-magic measure
computed at the operator level (Cao et al.), beyond this scaffold — demoted to
tracked/external. With E′ closed, all active coordinates for the session are
exhausted.
