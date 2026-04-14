# 사용자 제공 필요 가이드라인 목록

WebSearch로 전문을 충분히 수집하지 못한 가이드라인 목록. 사용자가 PDF 파일을 직접 제공하면 해당 파일의 내용을 보강한다.

> **참고**: 이 파일에는 ICH 관련 미수집 항목만 기재하였다. FDA, EMA, MFDS 관련 미수집 항목은 각 에이전트 결과 취합 후 추가 예정.

---

## 제공 필요 항목

| # | 가이드라인 | 기관 | 이유 | 파일 위치 | 보강 대상 항목 |
|---|----------|------|------|---------|--------------|
| 1 | ICH E6(R3) Step 4 최종본 전문 | ICH | PDF가 이미지 기반으로 텍스트 추출 불가. Annex 1 Appendix B 전체 조항 번호 및 세부 요건 원문 확인 필요 | `ich/ich_e6_r3.md` | Appendix B 전체 조항 원문, 용어집(Glossary) 신규 정의, Appendix C 필수 기록 목록 |
| 2 | ICH E8(R1) Step 4 최종본 전문 | ICH | PDF가 이미지 기반으로 텍스트 추출 불가. Section 7 CtQ 요소 전체 목록(18개) 원문 확인 필요 | `ich/ich_e8_r1.md` | Section 7 CtQ 요소 전체 목록 원문, 각 섹션 세부 내용 |
| 3 | ICH E14/S7B Q&A Step 4 전문 (2022.02) | ICH | PDF 이진 데이터로 텍스트 추출 불가. 5.1 접근법, 6.1 접근법, 이중 음성 통합 평가 세부 요건 원문 확인 필요 | `ich/ich_e14_qtc.md` | Q&A 5.1, 6.1 조항 원문, 이중 음성 통합 평가 세부 기준, S7B 비임상 연계 요건 |
| 4 | ICH E14 원본 가이드라인 전문 (2005) | ICH | PDF 이진 데이터로 텍스트 추출 불가. TQT 시험 설계 원칙 및 원문 표현 확인 필요 | `ich/ich_e14_qtc.md` | 원본 TQT 설계 조항, 양성 대조군 원문 요건 |
| 5 | ICH M13A Step 4 최종본 전문 (2024.07) | ICH | PDF 이진 데이터로 텍스트 추출 불가. BE 수용 기준, 식사 조건, 통계 분석법 원문 확인 필요 | `ich/ich_m13_bioequivalence.md` | 수용 기준 원문, 고변동 약물 정의 원문, 통계 분석법 세부 조항 |
| 6 | ICH E9(R1) Statistical Principles (Estimand) | ICH | 미수집 (임상시험 통계 설계 및 추정값 프레임워크) | 파일 미생성 | 추정값(Estimand) 정의, 민감도 분석, 통계 원칙 전반 |
| 7 | ICH E17 Multi-Regional Clinical Trials (MRCT) | ICH | 미수집 (다지역 임상시험 설계 원칙) | 파일 미생성 | MRCT 설계 원칙, 지역 데이터 평가, 일관성 분석 |
| 8 | ICH M9 BCS-based Biowaivers | ICH | 부분 정보만 수집 (M13A 연계 필수 문서). BCS Class I, III biowaiver 세부 기준 필요 | 파일 미생성 | BCS 분류 기준, 용해성/투과성 임계값, Biowaiver 신청 요건 |

---

## 메인 에이전트 추가 예정 항목

다음은 ICH 외 에이전트(FDA, EMA, MFDS 에이전트)가 각자 결과를 취합한 후 이 파일에 추가할 항목:

| 기관 | 추가 예정 항목 (예시) |
|------|---------------------|
| **FDA** | 집단 PK 가이드라인, 신장/간 기능 저하 시험 가이드라인, 소아 가이드라인 |
| **EMA** | 집단 PK 가이드라인, 특수 집단 가이드라인, ICH E6(R3) 이행 가이드 |
| **MFDS** | ADME 가이드라인, 동의설명서 작성 가이드, 특수 집단 가이드라인 |

---

## 제공 방법

1. 사용자가 PDF 파일을 다운로드
2. 파일을 이 프로젝트 디렉토리에 업로드하거나 경로를 제공
3. 에이전트가 파일을 읽고 해당 `.md` 파일의 `[전문 미수집 — 사용자 PDF 제공 필요]` 섹션을 보강

### ICH 공식 다운로드 링크

| 가이드라인 | 다운로드 URL |
|----------|-------------|
| E6(R3) 최종본 | https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf |
| E8(R1) 최종본 | https://database.ich.org/sites/default/files/ICH_E8-R1_Guideline_Step4_2021_1006.pdf |
| E14 원본 | https://database.ich.org/sites/default/files/E14_Guideline.pdf |
| E14/S7B Q&A 2022 | https://database.ich.org/sites/default/files/E14-S7B_QAs_Step4_2022_0221.pdf |
| M13A 최종본 | https://database.ich.org/sites/default/files/ICH_M13A_Step4_Final_Guideline_2024_0723.pdf |
| E9(R1) | https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1120.pdf |
| E17 | https://database.ich.org/sites/default/files/E17EWG_Step4_2017_1116.pdf |
| M9 | https://database.ich.org/sites/default/files/M9_EWG_Step4_Guideline_2020_0319.pdf |
