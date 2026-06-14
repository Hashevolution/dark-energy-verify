# dark-energy-verify

DESI DR2 암흑에너지 변칙 검증 작업장.

## 배경

상대성-양자역학 충돌을 "단일 실재의 관점적 사영"으로 본 직관에서 출발해
모듈러 이론·레인보우 사슬·관측 엔트로피까지 형식화했으나, 모두 선행연구와 겹쳤다.
전체 여정은 [`notes/monistic-relationalism-note.md`](notes/monistic-relationalism-note.md),
빠른 재개용 요약은 [`notes/handoff-summary.md`](notes/handoff-summary.md).

도달한 방법론:
> 직관만으로 풀면 계속 기존 이론에 매칭된다.
> 실제 관측 변칙 중 기존 법칙으로 설명 안 되는 것에서 출발해야 새 이론이 가능하다.

→ 본 레포는 그 첫 표적인 **DESI DR2 동역학적 암흑에너지 신호 (2.8σ~4.2σ)** 의 진위를
독립 재계산으로 검증한다.

## 검증할 질문

신호의 표본 의존(Pantheon+ / Union3 / DES-SN5YR에서 σ가 다름)이
**물리(진짜 변칙)** 인가 **계통오차(보정 차이)** 인가?

## 디렉토리

- `notes/` — 직관 → 형식화 → 변칙으로의 방향 전환 기록.
- `analysis/` — 검증 코드 (σ 재계산, 표본 비교, 공분산 분석).
- `data/` — DESI 공개 데이터 (체인·공분산). 대용량은 git LFS 또는 .gitignore.

## 다음 동작

1. 세 초신성 표본별 (w₀, wₐ) 중심값·오차·공분산 확보.
2. (−1, 0)으로부터 σ 직접 재계산.
3. DESI 발표값(2.8~4.2σ) 재현 확인.
4. 표본 간 차이가 통계인지 계통인지 분해.

## 참고

- DESI DR2 II: [arXiv:2503.14738](https://arxiv.org/abs/2503.14738)
- DESI DR2 확장 DE: [arXiv:2503.14743](https://arxiv.org/abs/2503.14743)
