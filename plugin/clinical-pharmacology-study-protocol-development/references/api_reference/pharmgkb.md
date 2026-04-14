# PharmGKB / ClinPGx API 레퍼런스

PharmGKB (Pharmacogenomics Knowledgebase)는 약물-유전자 상호작용의 대표 DB. 2026년 **ClinPGx** 플랫폼으로 통합되었으며 기존 도메인도 유효하다. translational-scientist가 약물유전체(PG) 조사에 사용한다.

## 기본 정보

| 항목 | 내용 |
|------|------|
| Base URL | `https://api.pharmgkb.org/v1/` |
| 인증 | **불필요** (공개 API) |
| 응답 형식 | JSON (`{"data":[...], "status":"success"}`) |
| Rate Limit | **2 req/sec** (초과 시 HTTP 429; 대량 사용 시 api@clinpgx.org 통보) |
| 라이선스 | **CC BY-SA 4.0** (학술·상업 모두 가능, 출처 표시·동일 조건 배포 요구) |
| Swagger | https://api.pharmgkb.org/swagger/ |
| 웹 리소스 | https://www.clinpgx.org/page/webResources |

## 주요 엔드포인트

### 1. 약물(Chemical) 정보

```
GET /v1/data/chemical?name={drug_name}
GET /v1/data/chemical/{chemicalId}
```

반환: 약물명, InChI/SMILES, prodrug 여부, 관련 유전자 목록

### 2. 유전자 정보

```
GET /v1/data/gene?symbol={GENE_SYMBOL}
GET /v1/data/gene/{geneId}
```

예: `/v1/data/gene?symbol=CYP2C19`

반환: 유전자 정보, VIP(Very Important Pharmacogene) 분류, 염색체 위치, 관련 약물

### 3. 임상 Annotation (가장 중요)

```
GET /v1/data/clinicalAnnotation
  ?view=mostRecent
  &chemical.accessionId={PA_ID}
  &gene.accessionId={PA_ID}
```

반환: 임상적으로 의미 있는 유전자-약물-변이 조합에 대한 annotation. **근거 등급 Level 1A/1B/2A/2B/3/4** 포함.

### 4. 가이드라인 (CPIC/DPWG)

```
GET /v1/data/guideline
  ?chemical.accessionId={PA_ID}
  &source={CPIC|DPWG|FDA|EMA}
```

반환: 표현형별(PM/IM/EM/UM) 용량 조절 권고 가이드라인

### 5. 변이 Annotation

```
GET /v1/data/variantAnnotation?variant.name={rsID}
```

예: `/v1/data/variantAnnotation?variant.name=rs4244285` (CYP2C19*2)

### 6. 약물 라벨 PGx 정보

```
GET /v1/data/label?source={FDA|EMA|PMDA|HCSC}
```

FDA/EMA 등 규제 당국이 라벨에 포함한 PGx 정보. **translational-scientist가 regulatory-expert의 DailyMed 조사와 교차 검증** 가능.

## WebFetch 쿼리 레시피

### 레시피 A: 유전자-약물 쌍의 임상 annotation 조회

```
WebFetch(
  url="https://api.pharmgkb.org/v1/data/clinicalAnnotation?view=mostRecent&chemical.name=clopidogrel&gene.symbol=CYP2C19",
  prompt="각 annotation의 level (Level 1A~4), 표현형(예: CYP2C19 PM/IM/EM/UM), 약물 반응 효과(감소/증가), 관련 PMID를 표로 추출"
)
```

### 레시피 B: 약물의 모든 PGx 가이드라인 조회

```
WebFetch(
  url="https://api.pharmgkb.org/v1/data/guideline?chemical.name=warfarin&source=CPIC",
  prompt="각 guideline의 제목, 관련 유전자(VKORC1, CYP2C9 등), 표현형별 용량 권고, 권고 등급(strong/moderate/optional), 가장 최근 업데이트 날짜를 추출"
)
```

### 레시피 C: 유전자의 VIP 정보

```
WebFetch(
  url="https://api.pharmgkb.org/v1/data/gene?symbol=CYP2D6",
  prompt="VIP(Very Important Pharmacogene) 여부, 주요 대립유전자(star alleles), 염색체 위치, 관련 약물 상위 10개 목록 추출"
)
```

### 레시피 D: 약물 라벨의 PGx 권고 (규제 기관별)

```
WebFetch(
  url="https://api.pharmgkb.org/v1/data/label?source=FDA&chemical.name=codeine",
  prompt="FDA 라벨의 PGx 권고 내용(CYP2D6 관련), 권고 수준(testing required/recommended/informative), 라벨 섹션 인용 추출"
)
```

## 필드 가이드 (임상시험 하네스 활용)

| 조사 목적 | 사용 엔드포인트 | 주요 반환 필드 |
|---------|--------------|--------------|
| DDI 시험 probe 선정 | `/gene` + `/clinicalAnnotation` | 대사 효소의 VIP 분류, 주요 annotation |
| PM/EM 빈도 관련 문헌 | `/clinicalAnnotation` | 관련 PMID 리스트 (PubMed로 추가 조사) |
| 표현형별 용량 조절 | `/guideline?source=CPIC` | CPIC 표현형 권고 |
| FDA 라벨 PGx 섹션 교차 검증 | `/label?source=FDA` | 라벨 공식 권고 (DailyMed 보완) |
| 변이 (rs번호) 조회 | `/variantAnnotation` | 변이별 약물 반응 annotation |

## 한국인 데이터 주의사항

**PharmGKB는 한국인 집단별 대립유전자 빈도를 구조화하여 제공하지 않는다.** 주요 빈도 데이터는 분산된 PubMed 문헌에 있음.

**권장 이중 전략:**
1. **PharmGKB**: 가이드라인·메커니즘·근거 등급·약물-유전자 관계 획득
2. **PubMed (MCP)**: 한국인 빈도 문헌 별도 조사
   - 예시 쿼리: `"CYP2C19 polymorphism Korean" OR "CYP2D6 allele frequency Korean"`
   - 주요 참조: 14,490명 코호트 (medRxiv), Frontiers Pharmacol 2024 등

## 산출물 저장 형식

`_workspace/01_references/pharmacogenomics/{gene_name}_{drug_name}.md`:

```markdown
# {유전자명} × {약물명} — PharmGKB

## 출처
- PharmGKB clinical annotation ID: CA{xxxxx}
- URL: https://www.clinpgx.org/clinicalAnnotation/{ID}
- 조회일: YYYY-MM-DD
- 라이선스: CC BY-SA 4.0

## 근거 등급
- Level: 1A / 1B / 2A / 2B / 3 / 4
- 근거: {요약}

## 표현형별 영향
| 표현형 | 약물 반응 | 권고 |
|-------|---------|------|
| PM (Poor Metabolizer) | ... | ... |
| IM (Intermediate) | ... | ... |
| EM (Extensive/Normal) | ... | ... |
| UM (Ultra-rapid) | ... | ... |

## 관련 PMID
- PMID: xxx
- PMID: xxx

## 본 시험 적용
- 한국인 빈도: (PubMed 별도 조사 결과 연계)
- 계획서 섹션별 활용 방안
```

## Gotchas

- **Rate limit 2 req/sec**: 429 응답 시 지수 백오프. 여러 약물을 조사할 때는 호출 간격 확보
- **AccessionId vs name**: PharmGKB는 PA ID(예: `PA448463`)로 내부 식별. `name` 쿼리는 가능하지만 정확도 낮음. 첫 호출로 ID 획득 후 후속 쿼리에 사용 권장
- **`view=mostRecent` 사용**: 과거 버전까지 반환하면 응답 크기 큼. 최신본만 필요하면 반드시 지정
- **2026년 ClinPGx 리브랜드**: URL과 일부 필드명이 변경될 수 있음 (예: `pharmgkbid` → `clinpgxid` 컬럼 리네임). 404 에러 시 https://blog.clinpgx.org 공지 확인
- **MFDS 라벨 PGx**: `/label?source=MFDS`는 **미지원**. 한국 라벨의 PGx 정보는 의약품안전나라 별도 조사 필요
- **CPIC 가이드라인은 PharmGKB에도 등록**: PharmGKB `/guideline?source=CPIC`로 조회 가능하나, CPIC 고유 데이터(diplotype→phenotype lookup 등)는 CPIC API가 더 직접적 (`cpic.md` 참조)

## 참고 링크

- Swagger 문서: https://api.pharmgkb.org/swagger/
- 전체 데이터셋 다운로드: https://www.clinpgx.org/downloads
- API 소개 블로그: https://blog.clinpgx.org/
