# 연말정산 스킬 설계서

## 1. 개요

| 항목 | 내용 |
|------|------|
| 스킬명 | `year-end-tax` |
| 도메인 | `hr` |
| 경로 | `skills/hr/year-end-tax/` |
| 대상 사용자 | 원천징수의무자 (회사 인사/급여 담당자) + 근로소득자 (직원 개인) |
| 동작 방식 | 모드 선택형 Q&A + 정제된 참조 지식베이스 + Python 계산기 |
| 원본 참조 | `docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf` |

## 2. 아키텍처

### 2.1 핵심 구조

```
skills/hr/year-end-tax/
├── SKILL.md                      # 진입점, 모드 선택, 라우팅 인덱스, Q&A 규칙
├── ref/                          # PDF에서 정제한 카테고리별 참조 자료
│   ├── 01-income-types.md        # 근로소득 유형/비과세
│   ├── 02-basic-deductions.md    # 인적공제 (기본/추가)
│   ├── 03-insurance.md           # 보험료 공제
│   ├── 04-medical.md             # 의료비 공제
│   ├── 05-education.md           # 교육비 공제
│   ├── 06-housing.md             # 주택 관련 공제
│   ├── 07-donation.md            # 기부금 공제
│   ├── 08-card-cash.md           # 신용카드/현금영수증
│   ├── 09-pension.md             # 연금/퇴직연금
│   ├── 10-tax-rates.md           # 세율표/계산 기준
│   ├── 11-process-employer.md    # 원천징수의무자 절차
│   └── 12-process-employee.md    # 근로자 절차/일정
├── calculators/                  # Python 계산 스크립트
│   ├── constants.py              # 연도별 세율표, 공제한도 등 상수
│   ├── income_tax.py             # 근로소득세 산출 (과세표준 -> 세액)
│   ├── personal_deduction.py     # 인적공제 계산
│   ├── insurance_deduction.py    # 보험료 공제
│   ├── medical_deduction.py      # 의료비 공제
│   ├── education_deduction.py    # 교육비 공제
│   ├── housing_deduction.py      # 주택 관련 공제
│   ├── donation_deduction.py     # 기부금 공제
│   ├── card_deduction.py         # 신용카드/현금영수증 공제
│   ├── pension_deduction.py      # 연금/퇴직연금 공제
│   ├── total_calculator.py       # 최종 환급/추가납부 통합 계산
│   └── tests/
│       └── test_*.py             # 각 계산기별 단위 테스트
├── COVERAGE.md                   # PDF 대비 커버리지 검증 문서
└── UPDATE-GUIDE.md               # PDF 갱신 시 작업 절차
```

### 2.2 데이터 흐름

```
[스킬 호출] → SKILL.md 로드
    │
    ├─ 모드 선택
    │   ├─ "전체 점검" (위자드 모드)
    │   │     사용자 유형 파악 (담당자/근로자)
    │   │     → 순차적으로 각 카테고리 질문
    │   │     → 해당 ref 읽기 + calculator 실행
    │   │     → 최종 요약 제공
    │   │
    │   └─ "특정 항목 문의" (자유 질의 모드)
    │         질문 파악 → 라우팅 테이블 매칭
    │         → 해당 ref만 읽기
    │         → 필요시 calculator 실행
    │         → 출처 포함 답변
    │
    └─ 공통 규칙
        - 수치 답변 시 반드시 [p.XX] 출처 표기
        - 확신 없는 내용은 "PDF 원문 확인 필요" 표기
        - 계산 결과는 calculator 실행 결과로 제공
```

## 3. SKILL.md 라우팅 인덱스

| 주제 | 키워드 | 참조 파일 | 계산기 |
|------|--------|----------|--------|
| 근로소득/비과세 | 급여, 비과세, 식대, 차량 | ref/01-income-types.md | income_tax.py |
| 인적공제 | 부양가족, 기본공제, 추가공제, 경로우대 | ref/02-basic-deductions.md | personal_deduction.py |
| 보험료 | 건강보험, 고용보험, 보장성보험 | ref/03-insurance.md | insurance_deduction.py |
| 의료비 | 병원비, 약값, 난임, 안경 | ref/04-medical.md | medical_deduction.py |
| 교육비 | 학원, 대학, 유치원, 교복 | ref/05-education.md | education_deduction.py |
| 주택 | 월세, 전세, 주택청약, 장기주택저당 | ref/06-housing.md | housing_deduction.py |
| 기부금 | 법정기부금, 지정기부금, 종교단체 | ref/07-donation.md | donation_deduction.py |
| 신용카드/현금 | 카드, 체크카드, 현금영수증, 전통시장 | ref/08-card-cash.md | card_deduction.py |
| 연금 | 국민연금, 퇴직연금, 개인연금, IRP | ref/09-pension.md | pension_deduction.py |
| 세율/산출 | 세율, 과세표준, 산출세액, 세액공제 | ref/10-tax-rates.md | income_tax.py |
| 원천징수 절차 | 신고, 제출, 지급명세서, 원천세 | ref/11-process-employer.md | - |
| 근로자 절차 | 간소화, 일정, 서류, 제출기한 | ref/12-process-employee.md | - |

## 4. 계산기 설계 원칙

- **순수 함수**: 입력 받고 결과 반환, 외부 의존성 없음
- **상수 분리**: 세율/한도 등 연도별 변동값은 `constants.py`로 분리
- **불변성**: 입력 데이터를 변경하지 않고 새 결과 객체를 반환
- **출처 포함**: 각 함수 docstring에 PDF 참조 페이지 명시
- **테스트 필수**: 모든 계산기에 단위 테스트 동봉

### constants.py 구조

```python
YEAR = 2025

# 소득세율 구간 [ref: p.XX]
TAX_BRACKETS = [
    (14_000_000, 0.06),
    (50_000_000, 0.15),
    (88_000_000, 0.24),
    (150_000_000, 0.35),
    (300_000_000, 0.38),
    (500_000_000, 0.40),
    (1_000_000_000, 0.42),
    (float('inf'), 0.45),
]

# 의료비 [ref: p.XX]
MEDICAL_DEDUCTION_RATE = 0.15
MEDICAL_DEDUCTION_RATE_INFERTILITY = 0.30
MEDICAL_LIMIT_GENERAL = 7_000_000

# ... 각 공제별 상수
```

## 5. 레퍼런스 정제 원칙

1. **원문 충실** - 해석/의역 없이 PDF 원문의 수치/조건/단서를 그대로 옮김
2. **출처 명시** - 모든 항목에 PDF 페이지 번호 기재 (예: `[p.42]`)
3. **조건 누락 방지** - "단, ~인 경우", "다만, ~에 해당하는 자는 제외" 등 예외 조건 반드시 포함
4. **담당자 검증** - 자동 추출 후 반드시 담당자가 PDF와 대조 리뷰

### ref 파일 포맷

```markdown
# [항목명] [ref: p.XX-YY]

## 공제 대상자
- 요건1 [p.XX]
- 요건2 [p.XX]

## 공제 대상
- 포함: ... [p.XX]
- **제외**: ... [p.XX]

## 공제 한도
- 조건별 한도 수치 [p.XX]

## 공제율
- 조건별 공제율 [p.XX]

## 예외/특이사항
- 단서 조항 [p.XX]

## 계산식
-> `calculators/XXX.py` 참조
```

## 6. PDF 갱신 워크플로우

```
[1] 국세청에서 새 PDF 배포
    → docs/ref/에 새 PDF 배치
         │
[2] 기존 ref 파일들과 대조하여 변경점 식별
    - 세율/한도 변경 → constants.py 업데이트
    - 새로운 공제 항목 → 신규 ref + calculator 추가
    - 폐지된 항목 → 해당 ref 아카이브 처리
         │
[3] ref 마크다운 갱신 (페이지 번호 재매핑)
         │
[4] calculator 테스트 실행 → 변경된 수치로 통과 확인
         │
[5] 커버리지 검증 문서(COVERAGE.md) 재생성
         │
[6] 담당자 리뷰 → 커밋
```

## 7. 커버리지 검증 문서 (COVERAGE.md)

### 레퍼런스 커버리지

| PDF 장/절 | 페이지 | ref 파일 | 반영 상태 | 비고 |
|-----------|--------|----------|----------|------|
| (PDF 분석 후 채움) | | | | |

### 계산식 커버리지

| 계산 항목 | PDF 위치 | 스크립트 | 테스트 | 검증 |
|-----------|----------|----------|--------|------|
| (PDF 분석 후 채움) | | | | |

### 미반영 항목 (의도적 제외)

| 항목 | 사유 |
|------|------|
| (PDF 분석 후 채움) | |

## 8. 위자드 모드 진행 순서

### 근로소득자 전체 점검

```
1. 기본정보 수집 (총급여, 가족 구성)
2. 인적공제 점검
3. 보험료 공제
4. 의료비 공제
5. 교육비 공제
6. 주택 관련 공제
7. 기부금 공제
8. 신용카드/현금영수증 공제
9. 연금 공제
10. 최종 세액 계산 (total_calculator.py)
11. 환급/추가납부 요약
```

### 원천징수의무자 신고 점검

```
1. 신고 일정 확인
2. 필수 제출 서류 체크리스트
3. 간소화 자료 수집 안내
4. 공제 신고서 검증 포인트
5. 원천세 신고/납부 절차
```
