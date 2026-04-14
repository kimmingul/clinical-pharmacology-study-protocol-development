# CPIC API 레퍼런스

CPIC (Clinical Pharmacogenetics Implementation Consortium)는 약물유전체 기반 임상 의사결정 가이드라인을 발행하는 국제 컨소시엄. **PostgREST 기반 공개 API**를 운영한다. translational-scientist가 표현형별 용량 조절 권고 조사에 사용한다.

## 기본 정보

| 항목 | 내용 |
|------|------|
| Base URL | `https://api.cpicpgx.org/v1/` |
| 인증 | **불필요** (공개 API) |
| API 형식 | PostgREST (RESTful, 필터·페이지네이션 표준) |
| 응답 형식 | JSON |
| 라이선스 | **CC0 1.0 Universal (Public Domain)** — 최고 자유도, attribution 권장 |
| 공식 사이트 | https://cpicpgx.org/ (→ https://www.clinpgx.org/ 리다이렉트) |
| GitHub | https://github.com/cpicpgx/cpic-data (활발히 유지 중) |

## PharmGKB와의 관계

2026년 CPIC·PharmGKB·ClinGen이 **ClinPGx 플랫폼으로 통합**되었다. 따라서:
- CPIC 가이드라인의 메타데이터는 **PharmGKB API로도 조회 가능** (`pharmgkb.md` 레시피 B 참조)
- **CPIC 고유 데이터**(diplotype→phenotype→recommendation lookup, 권고 등급 A/B/C/D)는 `api.cpicpgx.org`가 더 직접적
- 상황에 따라 두 API 중 선택 또는 병행 사용

## 주요 엔드포인트

PostgREST 기반이라 테이블/뷰를 직접 조회하는 형태.

### 1. 가이드라인 목록

```
GET /v1/guideline
GET /v1/guideline?name=eq.{guideline_name}
```

필터 문법: PostgREST 표준 (`eq.`, `like.`, `in.(...)` 등)

### 2. 약물-유전자 쌍 뷰

```
GET /v1/pair_view
GET /v1/pair_view?drugname=eq.{drug_name}
GET /v1/pair_view?genesymbol=eq.{gene_symbol}
```

반환: 약물-유전자 쌍별 CPIC 권고 등급(A/B/C/D), 가이드라인 링크

### 3. 권고 뷰 (핵심)

```
GET /v1/recommendation_view
GET /v1/recommendation_view?drugname=eq.{drug}&genesymbol=eq.{gene}
```

반환: 표현형(PM/IM/EM/UM)별 구체 용량 조절 권고, 강도(strong/moderate/optional), 분류(Avoid/Use with caution 등)

### 4. Diplotype → Phenotype 매핑

```
GET /v1/diplotype
GET /v1/diplotype?genesymbol=eq.CYP2C19
```

반환: 특정 유전자의 대립유전자 조합(diplotype)이 어떤 표현형으로 매핑되는지

### 5. Test Alert (용량 조정 알림)

```
GET /v1/test_alert_view
GET /v1/test_alert_view?drugname=eq.{drug}
```

반환: 약물 처방 시 유전형 검사 권고가 활성화되는 조건

## PostgREST 쿼리 문법

CPIC API는 **PostgREST**이므로 URL 파라미터로 SQL-like 필터링 가능:

| 연산자 | 의미 | 예시 |
|-------|------|------|
| `eq.` | 같음 | `?drugname=eq.warfarin` |
| `neq.` | 다름 | `?level=neq.D` |
| `like.` | LIKE (%는 `*`) | `?drugname=like.*warfarin*` |
| `ilike.` | 대소문자 무관 LIKE | `?drugname=ilike.*WARFARIN*` |
| `in.(...)` | IN | `?genesymbol=in.(CYP2C9,VKORC1)` |
| `gte.`, `lte.` | ≥, ≤ | 숫자/날짜 필드에서 |
| `or=(...)` | OR 조합 | `?or=(drugname.eq.warfarin,drugname.eq.aspirin)` |

**페이지네이션**: `Range` 헤더 또는 `limit`/`offset` 파라미터 (PostgREST 버전에 따라 지원)

## WebFetch 쿼리 레시피

### 레시피 A: 약물-유전자 쌍의 CPIC 권고 등급 확인

```
WebFetch(
  url="https://api.cpicpgx.org/v1/pair_view?drugname=eq.clopidogrel&genesymbol=eq.CYP2C19",
  prompt="반환된 JSON 객체의 cpiclevel (A/B/C/D), guideline 링크, 최종 업데이트 날짜를 추출"
)
```

### 레시피 B: 표현형별 용량 권고 조회

```
WebFetch(
  url="https://api.cpicpgx.org/v1/recommendation_view?drugname=eq.warfarin&genesymbol=in.(CYP2C9,VKORC1)",
  prompt="각 표현형 조합(예: CYP2C9 PM + VKORC1 GG)에 대한 권고(dosing guidance), 권고 강도(classification), 관련 문헌을 표로 정리"
)
```

### 레시피 C: 특정 유전자의 Diplotype → Phenotype 매핑

```
WebFetch(
  url="https://api.cpicpgx.org/v1/diplotype?genesymbol=eq.CYP2D6",
  prompt="CYP2D6의 주요 diplotype(예: *1/*1, *1/*4, *4/*4 등)과 각각의 phenotype(UM/NM/IM/PM) 매핑 표 추출. Activity score도 포함 시 함께 추출"
)
```

### 레시피 D: 대사효소의 모든 CPIC Level A 약물 목록

```
WebFetch(
  url="https://api.cpicpgx.org/v1/pair_view?genesymbol=eq.CYP2D6&cpiclevel=eq.A",
  prompt="CYP2D6 관련 CPIC Level A 약물 전체 목록, 각 약물의 권고 요약, 가이드라인 URL 추출"
)
```

## 주요 약물-유전자 쌍 (한국 임상시험 실무 중요)

| 유전자 | 약물 | CPIC Level | 한국인 PM 빈도 | 임상 의미 |
|-------|------|-----------|-------------|---------|
| CYP2C19 | Clopidogrel | A | ~15% | PM에서 항혈소판 효과 감소 |
| CYP2C19 | Voriconazole | A | ~15% | PM에서 과다 노출 |
| CYP2C19 | Proton pump inhibitors | A/B | ~15% | 산분비 억제 정도 차이 |
| CYP2D6 | Codeine | A | 낮음 (~1%) | UM에서 morphine 과다 생성 (위험) |
| CYP2D6 | Tamoxifen | A | 낮음 | UM/PM에서 항에스트로겐 효과 차이 |
| CYP2C9/VKORC1 | Warfarin | A | — | 용량 조절 필수 |
| TPMT/NUDT15 | Thiopurines | A | NUDT15 PM 동양인에 흔함 | 골수 억제 위험 |
| SLCO1B1 | Simvastatin | A | — | 근육 독성 위험 |
| HLA-B\*15:02 | Carbamazepine | A | 동양인에 존재 | SJS/TEN 위험 |

## 임상시험 하네스 활용 시나리오

### 1. DDI 시험 Probe 약물 선정 근거

```
DDI 시험에서 CYP2C19 probe로 omeprazole 사용
→ CPIC Level A 권고: CYP2C19 표현형별 용량 조정 확립
→ 계획서 "용량 설정 근거" 섹션에 CPIC 권고 인용
→ 선정 기준에 "CYP2C19 NM (Normal Metabolizer)만 포함" 또는
  "표현형별 stratification 수행"을 정당화
```

### 2. 선정/제외 기준 근거

```
Clopidogrel BE 시험 설계 시:
→ CPIC Level A: PM은 항혈소판 효과 크게 감소
→ 제외 기준에 "CYP2C19 PM 제외" 또는 "사전 유전형 검사" 정당화
```

### 3. ICF 약물유전체 동의 설명

```
시험대상자에게 유전형 검사 의미 설명 시:
→ CPIC 권고 인용 (예: "국제 가이드라인에 따르면 CYP2C19 유전형에 따라
  이 약의 효과가 다르게 나타날 수 있습니다")
→ ICF Part 4.1 PG 분석 동의 섹션의 근거로 CPIC 인용
```

## 산출물 저장 형식

`_workspace/01_references/pharmacogenomics/{drug}_{gene}_CPIC.md`:

```markdown
# {약물명} × {유전자명} — CPIC 권고

## 출처
- CPIC pair: https://api.cpicpgx.org/v1/pair_view?drugname=eq.{drug}&genesymbol=eq.{gene}
- Guideline URL: https://www.clinpgx.org/guidelineAnnotation/{id}
- 조회일: YYYY-MM-DD
- 라이선스: CC0 1.0

## CPIC Level
- {A/B/C/D}: {의미}

## 표현형별 권고
| 표현형 | 권고 | 강도 | 용량 조정 |
|-------|------|------|---------|
| PM | ... | strong/moderate/optional | ... |
| IM | ... | ... | ... |
| NM (EM) | ... | ... | ... |
| UM | ... | ... | ... |

## Diplotype → Phenotype 매핑 (주요)
| Diplotype | Phenotype |
|-----------|----------|
| ... | ... |

## 본 시험 적용
- 선정/제외 기준 반영:
- 용량 설정 근거:
- ICF 설명 문구:
```

## Gotchas

- **PostgREST 문법 주의**: `=eq.` (dot + 값), `=in.(...)`  — 일반 REST와 다름
- **약물명 소문자**: CPIC 데이터베이스는 소문자 저장이 일반적. `warfarin`은 동작하나 `Warfarin`은 결과 0
- **Level A만 인용**: Level A는 "CPIC 권고 발행, 근거 강함". 계획서 인용 시 **Level A/B만** 사용 권장. C/D는 "검토 단계"로 정식 권고 아님
- **2026년 컬럼명 변경**: `pharmgkbid` → `clinpgxid` 리네임 반영됨. 구 쿼리 재검토 필요
- **CPIC != PharmGKB**: CPIC은 PharmGKB의 하위 도구가 아닌 **독립 컨소시엄**. 출처 표기 시 구분
- **권고 업데이트**: 가이드라인은 새 증거 발견 시 개정됨. 인용 시 **액세스 날짜** 반드시 기록
- **MFDS 연계 없음**: CPIC은 미국·유럽 중심. 한국 MFDS 라벨에 CPIC 권고가 반영되지 않은 약물 다수. 한국 계획서 인용 시 "국제 가이드라인(CPIC)에 따르면…"으로 맥락 표시

## PharmGKB vs CPIC API 선택 가이드

| 조사 목적 | 권장 API |
|---------|--------|
| 약물-유전자 **근거 등급** | CPIC (Level A/B/C/D) — 더 명확 |
| 표현형별 **구체 용량 권고** | CPIC `recommendation_view` — 가장 직접적 |
| **Diplotype → Phenotype** 매핑 | CPIC `diplotype` — 고유 데이터 |
| 약물-유전자 **임상 annotation** (PMID 포함) | PharmGKB `clinicalAnnotation` |
| **변이(rs)별** annotation | PharmGKB `variantAnnotation` |
| 규제 기관(FDA/EMA) **라벨 PGx** | PharmGKB `label` |
| 유전자 메타데이터 (VIP 분류 등) | PharmGKB `gene` |

## 참고 링크

- API 루트: https://api.cpicpgx.org/v1/
- CPIC 가이드라인 목록: https://www.clinpgx.org/cpic/guidelines
- API·DB 문서: https://cpicpgx.org/api-and-database/
- GitHub 조직: https://github.com/cpicpgx
- 데이터 저장소: https://github.com/cpicpgx/cpic-data
- API 업데이트 블로그: https://blog.clinpgx.org/
