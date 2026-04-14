# MFDS 국내 임상시험 승인현황 — Clopidogrel

## 조회 정보

| 항목 | 내용 |
|------|------|
| 검색일 | 2026-04-14 |
| 출처 | https://nedrug.mfds.go.kr/searchClinic |
| 검색 파라미터 (영문) | searchType=ST1, searchKeyword=clopidogrel, approvalDtStart=2020-01-01, approvalDtEnd=2025-12-31 |
| 검색 파라미터 (한글) | searchType=ST1, searchKeyword=클로피도그렐, approvalDtStart=2015-01-01, approvalDtEnd=2025-12-31 |
| 영문 검색 결과 | **0건** |
| 한글 검색 결과 | **0건** |
| 추가 검색 (ST4/의뢰자) | 0건 |
| 상태 | **[MFDS 승인현황 미수집 — 오프라인 확인 권장]** |

---

## 조회 실패 원인 분석

1. **searchClinic HTML 파싱 문제**: WebFetch가 서버 렌더링 HTML에서 실제 검색 결과 데이터를 파싱하지 못함. 페이지 구조상 JavaScript로 동적 로딩되는 테이블이 있을 가능성.
2. **URL 인코딩 이슈**: 한글 키워드("클로피도그렐", "혈소판") URL 인코딩 처리 결과 0건.
3. **항혈소판 키워드 검색**: ST3(시험 제목) 검색어 "항혈소판", "혈소판" 모두 0건 반환.
4. **폴백 전략 미적용**: WebSearch 폴백은 공식 통계 아님 — 오프라인 확인 권장.

---

## 폴백: 공개 데이터 기반 국내 현황 추정

WebFetch 조회 실패에 따라 공개된 문헌 및 기존 지식 기반으로 국내 현황을 추정한다.

### Clopidogrel 관련 국내 임상 동향 (추정)

| 항목 | 내용 |
|------|------|
| 국내 허가 현황 | Clopidogrel 75 mg 정제는 국내 다수 제약사(한국BMS, 국내 제네릭사 포함) 허가 보유 |
| 적응증 | 급성관상동맥증후군, 죽상경화성 사건 예방 — 심장내과 분야 주요 약물 |
| CYP2C19 DDI 관련 국내 연구 관심도 | 높음 — 한국인 CYP2C19 PM 비율(~15%) 높아 임상적 중요성 크다고 알려짐 |
| DDI 관련 Phase 1 시험 (추정) | 국내 Phase 1 임상시험 수탁기관(SMO)에서 유사 설계 시험 수행 사례 있을 것으로 추정 |
| MFDS 심사 기준 | 2015년 약물상호작용 평가 가이드라인 기반 |

### 국내 관련 논문 (참고)

한국 연구자들에 의한 CYP2C19–Clopidogrel 관련 임상 연구가 다수 발표된 것으로 알려져 있음 (clinical-pharmacologist 담당 문헌 조사 결과 참조).

---

## 권고 사항

1. **오프라인 확인**: MFDS 의약품안전나라 직접 접속 (https://nedrug.mfds.go.kr/searchClinic)하여 "클로피도그렐" 또는 "약물상호작용" 키워드로 검색
2. **data.go.kr API**: 공공데이터포털 MFDS 임상시험 승인현황 API (서비스키 필요) 활용 검토
3. **연간 보고서**: MFDS 임상시험 승인 현황 연간 통계 보고서 (MFDS 홈페이지 발행) 참조
4. **ClinicalTrials.gov 보완**: `country=South Korea`, `intervention=clopidogrel`, `phase=Phase 1`으로 NCT 검색 — 한국에서 실시된 관련 시험 파악 가능

---

## ClinicalTrials.gov 국내 관련 시험 (clinical-pharmacologist 담당)

ClinicalTrials.gov에서 한국 실시 clopidogrel-omeprazole DDI 또는 CYP2C19-clopidogrel 관련 시험 검색은 clinical-pharmacologist가 별도 수행.

---

## 참고 문헌

- MFDS 의약품안전나라 임상시험 승인현황 검색 (https://nedrug.mfds.go.kr/searchClinic) — 2026-04-14 조회, 0건 반환
- [MFDS 승인현황 미수집 — 오프라인 확인 권장]
