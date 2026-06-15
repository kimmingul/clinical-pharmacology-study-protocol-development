# QA Fix Plan — Phase 9 수렴 루프 iteration 1

대상: `_workspace/03_protocol_draft.md`
critic: doc_lint --score (결정적 채점)
불변 입력 보존: 2×2 crossover, clopidogrel 300mg 부하+75mg, omeprazole 80mg, 단방향 omeprazole→clopidogrel 활성대사체 PK

| # | 심각도 | critic 보고 | 위치 | 수정 방향 |
|---|--------|------------|------|-----------|
| 1 | CRITICAL | ICH E6(R3) Appendix B 섹션 누락 (B.14, B.15, B.16; 13/16) | 문서 말미 | 신규 섹션 3개 추가 — `## B.14 Data Handling and Record Keeping`, `## B.15 Financing and Insurance`, `## B.16 Publication Policy` |
| 2 | CRITICAL | 보존기간 3년 기재 (KGCP 15년 필수) | B.12 "보존 기간은 3년으로 한다." | 해당 잘못된 문장 제거. 보존기간 진술은 신규 B.14로 이관하여 "최소 15년" 명시 |
| 3 | CRITICAL | goal_spec required ICH section 누락 (B.14~B.16) | required_ich_sections | #1 추가로 16개(B.1~B.16) 전부 `## B.N` 헤더 충족 |
| 4 | CRITICAL | 보존연한 3년 < goal_spec 최소(15년) | retention_years_min=15 | B.14에 "최소 15년" 명시 (KGCP·의약품등의 안전에 관한 규칙 별표 4 근거) |
| 5 | MAJOR | 90% CI/동등성 언급되나 '80.00'·'125.00' 경계 둘 다 미명시 | B.10 | B.10에 "90% 신뢰구간 80.00–125.00%" 판정 경계 명시 (no-effect/동등성 판정) |
| 6 | MINOR | 미해결 placeholder '[추가 정보 필요]' (washout) | B.4 | "[추가 정보 필요]" → "최소 14일 이상"으로 대체 + 반감기 근거 1문장 |

## 수정 근거 메모
- KGCP 보존기간: 의약품등의 안전에 관한 규칙 별표 4 (KGCP), 최소 15년 (규제 상수표 기본값)
- CI 경계: MFDS/FDA DDI no-effect 판정 표준 90% CI 80.00–125.00% (goal_spec acceptable_ci_bounds와 일치)
- Washout: clopidogrel 모약물 t½ ~6h, 활성대사체 t½ ~30분, omeprazole t½ ~0.5–1h이나 비가역적 혈소판 저해·CYP2C19 효소 회복(저해 해소까지 수일) 및 PK carry-over 방지를 고려해 보수적으로 최소 14일 이상 설정
