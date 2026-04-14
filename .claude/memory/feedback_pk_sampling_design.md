---
name: PK sampling and truncated AUC principles
description: PK 채혈시점과 휴약기는 반드시 Tmax/t½/AUC 등 PK 파라미터에 근거하여 산출. t½ > 24h인 장반감기 약물은 절단 AUC(AUC₀₋₇₂ₕ) 적용 검토.
type: feedback
---

채혈시점·휴약기는 PK 파라미터 근거로 명확히 산출할 것. 절단 AUC 해당 시 반드시 고려.

**Why:** E2E 테스트에서 초기 144h 채혈 설계가 과도하였고, 사용자가 72h 절단 AUC의 과학적 타당성을 지적. 채혈시점은 Tmax 기반 밀집, 소실기는 t½ 기반으로 설계해야 함.

**How to apply:**
- 채혈시점: Tmax 구간에 밀집 배치, 총 채혈 기간은 t½ 기반 (절단 AUC 적용 시 ~72h, 미적용 시 ≥3×t½)
- 휴약기: ≥10×t½(max)로 산출, 잔류 농도 < 0.1% Cmax 보장
- 절단 AUC 검토 조건: t½ > 24시간이면 AUC₀₋₇₂ₕ 적용 가능성 검토
- Synopsis와 Protocol에 산출 근거 테이블 필수 포함
