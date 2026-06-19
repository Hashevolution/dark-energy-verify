# 향후 연구 과제 선정 — 닫힌 자리·열린 자리 점검 → 다음 좌표 결정

> 목적: 지금까지 닫힌(검증 완료) 자리와 열린(미결) 자리를 점검하고, 레포 자체
> 기준으로 후보 과제를 평가해 **다음 연구 과제를 선정**한다.
> 입력 문서: `handover-emergent-spacetime.md`(과제 A/B/C/D),
> `task-A-B-connection-and-status.md`(최전선 합류 판정), `work-order-gap-hunt.md`(Phase 게이트),
> `analysis/README.md`(데이터 트랙 결과), `experiments/phase2*_RESULTS.md`(수치 트랙 결과).
> 작성일: 2026-06-19.

---

## 0. 한눈에 — 현재 좌표

| 과제 | 성격 | 현 상태 | 판정 |
|---|---|---|---|
| **A** de Sitter 빈칸 | 이론 | 이론 미착수. 2025–26 최전선 활발(arXiv:2508.14478 등) | **열림 (단독 아님 = 합류)** |
| **B** 메커니즘(magic) | 수치/이론 | Phase 2″ "재현 성공" → **§8 E 수행 중 소급 정정**: 실수-Clifford 통제군만 써서 magic 귀속 혼동 | **미결(입증·반증 둘 다 아님)** |
| **C** 신호 진위(DESI) | 데이터 | σ 재계산 완료(2.58/3.38/3.94 vs 2.8/3.8/4.2). 표본 일관. 잔차=컨벤션 | **거의 닫힘 / 잔여 분해 미완** |
| **D** 차별 카드(존재론) | 이론 | §9.8 monogamy 초과분 부호변화 = 측도 아티팩트인가 미결 | **열림 (작음, 유일 차별점)** |

**한 줄 요약:** B는 "올바른 무대에서 재현 성공"으로 *검증된 재발견* 패턴을 또 한 번 닫았고,
C는 "DESI 산수 맞고 표본 일관"으로 데이터 트랙의 핵심 질문에 답했다. A는 여전히 최전선
합류라 단독 차별이 어렵고, D는 작지만 *유일하게 살아남은 독창 후보*다.

---

## 1. 닫힌 자리가 가르쳐 준 것 (선정의 출발점)

### 1.1 C(데이터)에서 배운 것 — "신호는 진짜지만 우리 차별점은 거의 소진"
- σ 재계산(02): 2.58/3.38/3.94 → DESI 2.8/3.8/4.2와 **순서·크기 일치**, 잔차 0.2–0.4σ.
- 표본 간 텐션(03): 전 쌍 <2σ 하한, 차이벡터가 (w₀,wₐ) 축퇴선에 정렬 → **표본 일관**.
- 잔차 갭(04): 대부분 **marginal vs profile 컨벤션** 차이. 완전 매치는 11차원 cobaya
  profile 모드 필요 = **명시적으로 레포 범위 밖**.
- 번인(05): 갭 원인 아님(최대 0.035σ).
→ **남은 건 두 갈래뿐:** (i) 인프라 무거운 cobaya profile로 0.2–0.4σ를 *못박기*(확인용,
  차별성 낮음), (ii) README "next step 4"의 **통계 vs 계통 분해**(아직 진짜 미완).

### 1.2 B(수치)에서 배운 것 — "가설은 옳았으나 무대가 전부였고, 결과는 재현"
- Phase 2/2′(1D 사슬): full·비국소 magic 프록시 전부 임계도/얽힘으로 **환원** → 무대 틀림.
- Phase 2″(홀로그래픽 코드): 비국소 magic(CS 게이트) → 넓이연산자 **상태의존**, 클리퍼드
  (CZ, 얽힘만)는 자명 → **얽힘이 아니라 magic이 기하를 휘게 함** 격리 성공.
- 단, 이는 **Cao et al.(2306.14996) 재현**이지 새 물리 아님. 한계: 최소 2-텐서 코드.
→ 패턴 반복: 직관의 좌표는 정확히 확정됐으나, **또 기존 결과에 도달**.

### 1.3 두 닫힘의 공통 교훈
> A·B·C 어디서도 "기존을 넘는 잔차"는 안 남았다. 매번 *재발견*이거나 *최전선 합류*다.
> → 다음 선정의 1순위 기준은 **"아직 아무도 두 좌표를 잇지 않은 자리"**, 즉
> *교차점*이어야 한다. 단일 좌표는 전부 이미 밟혀 있다.

---

## 2. 선정 기준 (레포 자체 원칙에서)

| # | 기준 | 왜 |
|---|---|---|
| K1 | **차별성** | 또 다른 재발견/최전선 합류를 피하는가 (§1.3 교훈) |
| K2 | **자기완결성** | 외부 데이터·최전선 협업 없이 *지금* 실행 가능한가 |
| K3 | **레버리지** | 기존 자산(Phase 2″ 스캐폴드, DESI 체인) 재사용하는가 |
| K4 | **반증가능성** | 명확한 게이트로 자가반증(§9.15) 가능한가 — 통과/탈락 모두 산출 |

---

> **〔갱신 2026-06-19〕 과제 E 실행 완료 → (a)/혼동 판정. §8 참조.** 1순위는 **E′(더 큰
> 홀로그래픽 코드)** 로 이동. E는 de Sitter 손잡이(pseudo-entropy)는 구축했으나, 최소
> 2-텐서 코드에서 magic을 국소 복소 위상과 분리하지 못함. **부수효과: Phase 2″ 소급 강등.**

## 3. 후보 평가표

| 후보 | 내용 | K1 차별 | K2 자기완결 | K3 레버리지 | K4 반증 | 종합 |
|---|---|:---:|:---:|:---:|:---:|---|
| ~~**E** magic × de Sitter 교차~~ | Phase 2″ 코드를 de Sitter형(pseudo-entropy)으로 변형 → **실행 완료, (a)/혼동** (§8) | ★★★ | ★★★ | ★★★ | ★★★ | **실행됨 → E′로** |
| **E′** 큰 홀로그래픽 코드 | 단일-bond 위상이 *진짜 제거 가능*한 큰 HaPPY 코드에서 magic×de Sitter 재측정 | ★★★ | ★★ | ★★ | ★★★ | **신규 1순위** |
| **D** 존재론 카드 결판 | §9.8 monogamy 초과분 부호변화 = 측도 아티팩트 결판 | ★★★ | ★★★ | ★★ | ★★★ | **2순위 선정** |
| **C′** 통계 vs 계통 분해 | 표본 간 변이를 크기·z범위(통계) vs 보정(계통)으로 분해 (README step 4) | ★★ | ★★ | ★★★ | ★★ | **3순위 선정(데이터)** |
| B+ 코드 스케일업 | 큰 HaPPY 망에서 넓이연산자 스펙트럼 완전추출 | ★ | ★★★ | ★★★ | ★★ | 보류(확인용) |
| C+ cobaya profile | 11차원 profile로 0.2–0.4σ 못박기 | ★ | ★ | ★★ | ★ | 보류(인프라·확인용) |
| A° de Sitter EE 이론 | static patch/pseudo-entropy 직접 이론 구축 | ★★ | ★ | ★ | ★ | 추적만(최전선 합류) |

---

## 4. 선정 결과

### 1순위 〔선정〕 과제 E — **magic × de Sitter 교차** (A∩B 자리)

**왜 이것인가 (§1.3 교훈의 직접 귀결):**
- A(de Sitter 빈칸)와 B(magic 메커니즘)는 레포 안에서 **따로따로** 다뤄졌다.
  B는 전부 **AdS측 홀로그래픽 코드**(perfect tensor, 음곡률 무대)에서 검증됐고,
  A는 손도 안 댄 **양곡률**이다.
- **아직 아무도 잇지 않은 교차점:** "비국소 magic → 상태의존 넓이연산자"라는 B의
  메커니즘이 **양곡률(de Sitter형) 무대에서도 성립하는가, 아니면 깨지는가?"**
- 핸드오버 §3이 이미 가리킨 자리 — "여기서 (a)이론 빈칸과 (b)데이터 검증이 *만난다*".
  C가 de Sitter 동역학 신호의 진위를 (DESI 산수 기준) 확인해 줬으므로, **표적이 실재함**도
  보장된다.

**구체 계획 (Phase 2″ 자산 재사용):**
| 단계 | 방법 | 산출 |
|---|---|---|
| E.1 | Phase 2″ 코드의 안정자/CS 게이트 분리 진단을 **곡률 부호 다이얼**로 파라미터화 | baseline 재현 |
| E.2 | RT 표면이 **양곡률처럼 배치된** 텐서망(중심부 양곡률 = floral lattice류, task-A-B §2.3 참조)에서 동일 magic 주입 | Var(S_A) vs 곡률부호 |
| E.3 | 핵심 질문: de Sitter측에서 RT가 **강한 부분가법성 위반**(task-A-B §2.2)하는데, 그때 magic→상태의존 효과가 *살아남나/뒤집히나/사라지나* | 게이트 E |
| E.4 | 자가반증(§9.15): 게이트 분해(CZ/CS), region 스캔, 정규화 바꿔 응답 강건성 | 강건성 판정 |

**게이트 E:** magic→넓이연산자 효과의 **곡률 부호 의존성**이 존재하나?
- (b) **양곡률에서 효과가 질적으로 다름/깨짐** → 이것이 §1.2(2) "거울우주는 완벽, 진짜우주는
  절반"의 *수치적 정체* = 노트가 못 본 자리. **최초의 (b) 잔차 후보.**
- (a) 곡률 부호와 무관하게 동일 → 또 재발견. 그래도 "magic 메커니즘은 곡률 부호 불변"이라는
  **명확한 음성 결과**가 남음(= de Sitter 빈칸이 magic으로는 안 메워짐을 확정).

**정직한 위험:** 양곡률 텐서망에서 perfect-tensor 성질이 깨질 수 있어 baseline 재현 자체가
까다로울 수 있다. → E.1에서 *안정자 baseline이 양곡률 무대에서도 자명한지* 먼저 확인(게이트 0).
실패 시 무대 설계로 회귀. (Phase 2′의 "무대가 틀렸다" 교훈을 미리 차단.)

### 2순위 〔선정〕 과제 D — **존재론 카드 결판** (병행, 가벼움)

**왜:** 레포의 **유일하게 살아남은 독창 후보**(방법이 아닌 *존재론*). 닫아두면 차별성 전부
소멸. RQD(arXiv:2412.05979)에 포위됐으나 "단일 실재 고수 vs 부정"의 미세 분기는 아직 생존.
- **할 일:** §9.8 monogamy 초과분 **부호변화가 측도 아티팩트인가 실재인가** 수치 결판
  (Phase 2 스핀사슬 자산 재사용 가능 — 측도/정규화 바꿔 부호변화 강건성 1회 더).
- **자기완결·소규모.** E와 병행 가능. K1(차별)이 최고라 E가 (a)로 떨어져도 보험.

### 3순위 〔선정, 데이터 트랙〕 과제 C′ — **통계 vs 계통 분해**

**왜:** C에서 유일하게 *진짜* 남은 미완. "표본 일관"은 보였으나, 표본 간 변이를
**통계적(크기·z범위) vs 계통적(보정 절차)** 으로 분해하는 README step 4는 미수행.
- **할 일:** 03(표본 비교)을 확장 — 각 표본 σ를 z-범위·표본크기로 정규화했을 때 남는
  잔차가 *보정 절차 차이*에 정렬되나. DESI 공개 체인 재사용(K3).
- 우선순위 3위인 이유: C의 핵심 질문(진위)은 이미 답함 → 이건 *마감*이지 돌파 아님.
  단 E가 막힐 때 즉시 실행 가능한 독립 데이터 작업.

---

## 5. 보류·추적 목록 (선정 제외, 근거 명시)

| 항목 | 처리 | 근거 |
|---|---|---|
| **B+ 코드 스케일업** | 보류 | K1 낮음. 큰 HaPPY 망은 효과를 *풍부히* 하나 새 물리 아닌 확인. E가 더 차별적 |
| **C+ cobaya profile** | 보류 | 11차원 인프라 무겁고 *확인용*. 0.2–0.4σ는 이미 컨벤션으로 설명됨 |
| **A° de Sitter EE 직접 이론** | 추적만 | 최전선 합류(2508.14478/2506.06595/2604.00108). 단독 차별 불가. E가 *수치로* 같은 질문에 붙는 우회로 |
| **B(메커니즘 일반 이론)** | 추적만 | 분야 최대 난제, 비전공자 단독 불가(핸드오버 §3.B). 모니터만 |

---

## 6. 실행 순서 / 다음 액션

```
[즉시·자기완결]  E.1 양곡률 baseline 게이트0  ──┐
                                                 ├─→ 게이트 E (곡률부호 의존성)
[병행·가벼움]    D  부호변화 결판 1회 더        ──┘
[E 막히면 즉시]  C′ 통계 vs 계통 분해 (독립 데이터)
[추적만]         A° de Sitter EE 논쟁 통독, B 모니터
```

1. **〔1순위〕 E**: Phase 2″ 코드 → 양곡률 무대. **게이트 0(baseline 자명)** 먼저, 통과 시
   magic 주입 → **게이트 E(곡률 부호 의존성)**. 산출: "양곡률에서 magic→넓이 효과가
   X처럼 바뀐다/안 바뀐다" 정량 판정.
2. **〔2순위·병행〕 D**: §9.8 부호변화 측도-아티팩트 결판. 차별 카드 보존.
3. **〔E 정체 시〕 C′**: 표본 변이의 통계/계통 분해로 데이터 트랙 마감.
4. **〔추적〕 A°/B**: 통독·모니터, 직접 도전 보류.

**각 게이트 끝에서 반드시 1줄 판정 기록**(통과/탈락 a=재발견 / b=잔차생존) — `work-order`
규율 그대로. 탈락도 빈틈 지도다.

---

## 7. 한 줄 결론

> **선정: 1순위 E(magic × de Sitter 교차) — 아직 아무도 잇지 않은 A∩B 자리, 자기완결·반증가능.**
> 2순위 D(유일 차별 카드 보존), 3순위 C′(데이터 마감). B+/C+/A°는 보류·추적.
> 단일 좌표는 전부 밟혔다 → 다음은 **교차점**에서만 (b) 잔차가 나올 수 있다.

---

## 8. 〔실행 기록 2026-06-19〕 과제 E 수행 결과 → (a)/혼동, 1순위 E′로 이동

**실행:** `experiments/phaseE_desitter_magic.py`, `phaseE_selffalsify.py`,
`phaseE_confound_scan.py`. 상세: `experiments/phaseE_RESULTS.md`.

**무대·손잡이:** Phase 2″ 두 perfect-tensor 코드 재사용. 곡률 부호 다이얼 = pseudo-entropy
(비-에르미트 전이행렬)의 bra-ket 어긋남 각도 δ. δ=0=AdS(보통 엔트로피), δ>0=de Sitter형(복소).

**게이트 진행:**
- 게이트 0 + self-check **통과** — de Sitter 손잡이 자체는 작동(δ=0에서 보통 엔트로피와 정확 일치,
  안정자/실수-Clifford는 δ 전 구간 자명).
- 원시 게이트 E: magic(CS)이 dS측에서 **상태의존 허수 넓이**를 켬(Var(Im)∝δ²), AdS·비-magic엔 없음
  = 원시 (b)로 보였고 자가반증 T1–T5(축·측도·게이트·분기절단) 전부 통과.
- **결정적 통제(T6): 복소이되 magic=0인 Clifford 게이트(S⊗I 등)가 같은 효과를 *더 크게* 켬.**
  전수조사 결과 **magic을 분리하는 깨끗한 영역 0개.** → 최소 코드가 magic을 국소 복소 위상과
  분리 못 함 = 유한크기 아티팩트.

**판정:** **게이트 E = (a)/INCONCLUSIVE(혼동).** Phase 2 1차 판정 철회와 같은 실패 양식.

**부수효과 — Phase 2″ 소급 강등:** 원 Phase 2″는 **실수 Clifford(CZ) 통제군만** 썼다. 복소
Clifford를 넣으면 "상태의존=magic" 추론이 깨진다(S⊗I가 더 큼). → **노트의 magic 가설은 이
최소 코드에서 입증도 반증도 아닌 미결**(§0 표의 B "닫힘(재발견)"을 "미결"로 정정).

**살아남은 성과:** (1) 재사용 가능한 de Sitter pseudo-entropy 인프라, (2) §9.15 규율이 원시 (b)와
*과거* 과잉판정을 동시에 교정, (3) 다음 무대 정밀 확정.

**갱신된 우선순위:**
1. **〔신규 1순위〕 E′ — 더 큰 HaPPY 코드.** 단일-bond 위상이 *진짜 제거 가능*해지는 크기에서,
   안정자+실수+복소 Clifford 전 통제군 게이트 0′ 통과 후에만 magic 주입 → de Sitter 채널 재측정.
   (자기완결이나 구현 무거움.)
2. **〔재저울질로 승급 가능〕 D** — E′가 무거우므로, 가벼운 D(존재론 카드)를 병행/선행 후보로.
3. **〔데이터〕 C′** — 변함없이 독립 실행 가능.

> 교훈 재확인: **통제군 한 줄("복소이되 magic 아님")이 원시 (b)와 Phase 2″ 판정을 동시에 뒤집었다.**

---

## English summary

After closing the data track (C: DESI σ reproduces, samples consistent, residual gap is a
marginal-vs-profile convention) and the mechanism track (B: magic→area-operator
reproduced in AdS-side holographic codes, a verified rediscovery), every *single*
coordinate has turned out to be either a rediscovery or a frontier-merge. The selection
principle therefore shifts to **intersections nobody has joined yet**.

**Selected — Topic E (1st): magic × de Sitter.** B's mechanism ("non-local magic →
state-dependent area operator") was only ever verified on the *negative-curvature* (AdS)
stage; de Sitter (positive curvature, our universe) is untouched. Reusing the Phase-2″
scaffold, dial the curvature sign and ask whether the magic→geometry effect survives,
breaks, or flips on a de Sitter-like network. This sits exactly where the (a) theory gap
and (b) data verification meet, is self-contained, and is falsifiable either way.

**Also selected:** D (2nd, resolve the §9.8 sign-change — the only surviving original
differentiation card) and C′ (3rd, decompose inter-sample variation into statistical vs
systematic — the one genuinely unfinished piece of the data track). Deferred/tracked:
B-scaleup and full cobaya profiling (confirmatory), direct de Sitter EE theory
(frontier-merge).
