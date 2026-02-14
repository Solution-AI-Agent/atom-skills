---
name: year-end-tax
description: "2025 귀속 연말정산 Q&A 스킬. 원천징수의무자(회사 인사/급여 담당자)와 근로소득자(직원) 대상. 근로소득 비과세, 인적공제, 보험료, 의료비, 교육비, 주택, 기부금, 신용카드, 연금, 세율/산출세액 등 연말정산 전 항목을 다루며, Python 계산기로 정확한 세액 계산을 제공합니다. 국세청 PDF 원문 기반 [p.XX] 출처 포함 답변."
allowed-tools:
  - read
  - bash
  - glob
  - grep
---

# 연말정산 Q&A (Year-End Tax Settlement)

## 개요

2025 귀속 연말정산 가이드. 국세청 원천징수의무자를 위한 연말정산 신고안내 PDF(418p) 기반.

**대상:** 원천징수의무자 (회사 인사/급여 담당자) + 근로소득자 (직원 개인)

## 사용 모드

사용자에게 먼저 모드를 확인합니다:

### 1. 전체 점검 (위자드 모드)

사용자 유형에 따라 순차 진행합니다.

**근로소득자:**
1. 기본정보 수집 (총급여, 가족 구성)
2. 인적공제 점검
3. 보험료 공제
4. 의료비 공제
5. 교육비 공제
6. 주택 관련 공제
7. 기부금 공제
8. 신용카드/현금영수증 공제
9. 연금 공제
10. 최종 세액 계산 (`calculators/total_calculator.py` 실행)
11. 환급/추가납부 요약

**원천징수의무자:**
1. 신고 일정 확인
2. 필수 제출 서류 체크리스트
3. 간소화 자료 수집 안내
4. 공제 신고서 검증 포인트
5. 원천세 신고/납부 절차

### 2. 특정 항목 문의 (자유 질의 모드)

아래 라우팅 테이블을 참조하여 해당 ref 파일만 읽고 답변합니다.

## 라우팅 인덱스

질문에 해당하는 ref 파일을 읽고, 필요시 calculator를 실행합니다.

| 주제 | 키워드 | 참조 파일 | 계산기 |
|------|--------|----------|--------|
| 근로소득/비과세 | 급여, 비과세, 식대, 차량유지비, 출산지원금, 보육수당 | `ref/01-income-types.md` | `calculators/income_tax.py` |
| 인적공제 | 부양가족, 기본공제, 추가공제, 경로우대, 장애인, 한부모, 부녀자 | `ref/02-basic-deductions.md` | `calculators/personal_deduction.py` |
| 보험료 | 건강보험, 고용보험, 장기요양, 보장성보험 | `ref/03-insurance.md` | `calculators/insurance_deduction.py` |
| 의료비 | 병원비, 약값, 난임시술, 안경, 산후조리원, 실손보험 | `ref/04-medical.md` | `calculators/medical_deduction.py` |
| 교육비 | 학원, 대학, 유치원, 교복, 체험학습, 대학원, 수능 | `ref/05-education.md` | `calculators/education_deduction.py` |
| 주택 | 월세, 전세자금, 주택청약, 장기주택저당, 주택마련저축 | `ref/06-housing.md` | `calculators/housing_deduction.py` |
| 기부금 | 정치자금, 고향사랑, 특례기부금, 종교단체, 일반기부금 | `ref/07-donation.md` | `calculators/donation_deduction.py` |
| 신용카드/현금 | 신용카드, 체크카드, 현금영수증, 전통시장, 대중교통, 문화체육 | `ref/08-card-cash.md` | `calculators/card_deduction.py` |
| 연금 | 국민연금, 퇴직연금, 개인연금, IRP, 연금저축 | `ref/09-pension.md` | `calculators/pension_deduction.py` |
| 세율/산출 | 세율, 과세표준, 산출세액, 근로소득세액공제 | `ref/10-tax-rates.md` | `calculators/income_tax.py` |
| 자녀세액공제 | 자녀, 출산, 입양 | `ref/02-basic-deductions.md` | `calculators/personal_deduction.py` |
| 원천징수 절차 | 신고, 제출, 지급명세서, 원천세, 수정신고 | `ref/11-process-employer.md` | - |
| 근로자 절차 | 간소화서비스, 일정, 서류제출, 경정청구 | `ref/12-process-employee.md` | - |

## 계산기 사용법

계산이 필요한 질문에는 Python 계산기를 실행합니다.

**통합 계산 (전체 세액):**
```bash
cd skills/hr/year-end-tax && python -c "
from calculators.total_calculator import calc_year_end_tax
result = calc_year_end_tax(
    total_salary=65_400_000,
    num_dependents=4,
    national_pension=2_500_000,
    health_insurance=1_300_000,
    long_term_care=400_000,
    housing_loan_deduction=1_000_000,
    card_deduction=4_895_000,
    children_over_8=1,
    birth_orders=[3],
    pension_savings=2_000_000,
    retirement_pension=1_000_000,
    insurance_tax_credit=120_000,
    medical_tax_credit=950_700,
    education_tax_credit=630_000,
    donation_tax_credit=271_818,
    prepaid_tax=1_000_000,
)
for k, v in result.items():
    print(f'{k}: {v:,}')
"
```

**개별 항목 계산 예시:**
```bash
cd skills/hr/year-end-tax && python -c "
from calculators.income_tax import calc_earned_income_deduction, calc_calculated_tax
print('근로소득공제:', calc_earned_income_deduction(65_400_000))
print('산출세액:', calc_calculated_tax(36_285_000))
"
```

### 계산기 목록

| 모듈 | 주요 함수 | 용도 |
|------|----------|------|
| `income_tax.py` | `calc_earned_income_deduction()`, `calc_calculated_tax()`, `calc_earned_income_tax_credit()` | 근로소득공제, 산출세액, 근로소득세액공제 |
| `personal_deduction.py` | `calc_basic_personal_deduction()`, `calc_child_tax_credit()` | 인적공제, 자녀세액공제 |
| `insurance_deduction.py` | `calc_insurance_income_deduction()`, `calc_insurance_tax_credit()` | 보험료 소득공제, 세액공제 |
| `medical_deduction.py` | `calc_medical_tax_credit()` | 의료비 세액공제 |
| `education_deduction.py` | `calc_education_tax_credit()` | 교육비 세액공제 |
| `housing_deduction.py` | `calc_housing_loan_deduction()`, `calc_rent_tax_credit()` | 주택자금 소득공제, 월세 세액공제 |
| `donation_deduction.py` | `calc_donation_tax_credit()` | 기부금 세액공제 |
| `card_deduction.py` | `calc_card_deduction()` | 신용카드등 소득공제 |
| `pension_deduction.py` | `calc_pension_insurance_deduction()`, `calc_pension_tax_credit()` | 연금보험료 소득공제, 연금계좌 세액공제 |
| `total_calculator.py` | `calc_year_end_tax()` | 통합 세액 계산 (환급/추가납부) |

## 답변 규칙

1. **출처 필수**: 수치/조건 답변 시 반드시 `[p.XX]` 형식으로 PDF 페이지 출처를 포함합니다.
2. **계산기 우선**: 숫자 계산이 필요한 질문에는 반드시 Python 계산기를 실행하여 결과를 제공합니다.
3. **불확실성 표기**: ref 파일에 없는 내용은 "PDF 원문 확인이 필요합니다"라고 명시합니다.
4. **예외 조건 포함**: "단, ~인 경우 제외", "다만, ~에 해당하는 경우" 등 예외 조건을 빠짐없이 안내합니다.
5. **ref 선택적 로딩**: 질문에 해당하는 ref 파일만 읽습니다. 전체를 한꺼번에 읽지 않습니다.

## 상수 갱신 (연도별)

세율, 공제한도 등은 `calculators/constants.py`에 분리되어 있습니다. 세법 개정 시 이 파일만 업데이트하면 됩니다.

## 원본 자료

- PDF: `docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf` (418p)
- 과세연도: 2025 귀속
