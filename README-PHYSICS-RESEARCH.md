# 창발 시공간 / 암흑에너지 / magic 연구 (shor 레포에서 이동)

원래 실수로 `Hashevolution/shor` 레포에 작업됨 → `dark-energy-verify`로 이동.
이 묶음을 dark-energy-verify 루트에 그대로 풀면 경로가 맞습니다.

## 구성
연구 노트(루트):
- handover-emergent-spacetime.md      — 핸드오버 정리(상대성·양자 연결 현황, 과제 A/B/C/D)
- monistic-relationalism-note.md      — 원본 직관 사슬(일원론적 관계주의, 735줄)
- task-A-B-connection-and-status.md   — A(de Sitter)·B(메커니즘)로의 연결 + 연구현황 검증
- work-order-gap-hunt.md              — 작업순서(게이트 방식) + Phase별 판정

실험 코드/결과(experiments/):
- phase2_magic_curvature.py / phase2b_selffalsify.py / phase2_RESULTS.md
    Phase 2: 스핀사슬 magic vs 곡률 → (a) 임계도 재발견
- phase2prime_nonlocal_magic.py / phase2prime_results.txt
    Phase 2': 비국소 magic 프록시 → 1D에선 환원, 무대가 틀림
- phase2pp_holographic_magic.py / phase2pp_v2_nonlocal.py / phase2pp_v3_regionscan.py / phase2pp_RESULTS.md
    Phase 2'': 홀로그래픽 코드에서 비국소 magic → 상태의존 넓이연산자 재현 성공

## 실행
의존성: numpy, scipy  (pip install numpy scipy)
experiments/ 안에서 실행 (모듈이 서로 import 함):
    cd experiments
    python3 phase2_magic_curvature.py
    python3 phase2b_selffalsify.py
    python3 phase2prime_nonlocal_magic.py     # 무거움(~5분)
    python3 phase2pp_holographic_magic.py
    python3 phase2pp_v2_nonlocal.py
    python3 phase2pp_v3_regionscan.py
