# 연말정산 스킬 구현 계획 (Year-End Tax Skill Implementation Plan)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 국세청 연말정산 PDF를 기반으로 정확한 참조 지식베이스와 Python 계산기를 갖춘 연말정산 Q&A 스킬을 구축한다.

**Architecture:** SKILL.md가 라우팅 인덱스 역할을 하며, 사용자 질문에 따라 카테고리별 ref 마크다운만 선택적으로 읽고, 고정 수학식은 Python 스크립트로 실행하여 정확한 결과를 제공한다.

**Tech Stack:** Markdown (ref), Python 3 (calculators), pytest (tests)

**Source PDF:** `docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf` (418페이지)

**Design Doc:** `docs/plans/2026-02-14-year-end-tax-design.md`

---

## PDF 섹션 -> ref 파일 매핑

| ref 파일 | PDF 소스 | 페이지 범위 |
|----------|----------|------------|
| 01-income-types.md | 2부 Ⅰ. 근로소득 | p.50-79 |
| 02-basic-deductions.md | 2부 Ⅲ. 근로소득공제, 인적공제, 연금보험료공제 | p.94-104 |
| 03-insurance.md | 2부 Ⅳ §02 보험료공제 + 2부 Ⅵ §08 보험료 세액공제 | p.107, p.169-173 |
| 04-medical.md | 2부 Ⅵ §08 의료비 세액공제 | p.173-187 |
| 05-education.md | 2부 Ⅵ §08 교육비 세액공제 | p.187-195 |
| 06-housing.md | 2부 Ⅳ §03 주택자금공제 + 2부 Ⅴ §03 주택마련저축 + 2부 Ⅵ §09 월세 | p.107-119, p.122-123, p.202-204 |
| 07-donation.md | 2부 Ⅵ §08 기부금 세액공제 | p.195-201 |
| 08-card-cash.md | 2부 Ⅴ §05 신용카드 등 사용금액 소득공제 | p.132-138 |
| 09-pension.md | 2부 Ⅲ §03 연금보험료 + 2부 Ⅴ §01 개인연금 + 2부 Ⅵ §07 연금계좌 | p.103-104, p.120-121, p.164-168 |
| 10-tax-rates.md | 2부 전체 세율/산출 관련 + 2부 Ⅵ §04 근로소득세액공제 | p.94, p.162-163 |
| 11-process-employer.md | 1부 Ⅱ-Ⅲ 원천징수의무자 일정/확인사항 | p.27-48 |
| 12-process-employee.md | 1부 Ⅰ 간소화서비스 + 부록 1-3 | p.26, p.358-388 |

---

## Phase 1: 프로젝트 셋업

### Task 1: 디렉토리 구조 생성

**Files:**
- Create: `skills/hr/year-end-tax/ref/` (directory)
- Create: `skills/hr/year-end-tax/calculators/` (directory)
- Create: `skills/hr/year-end-tax/calculators/tests/` (directory)

**Step 1: 디렉토리 생성**

```bash
mkdir -p skills/hr/year-end-tax/ref
mkdir -p skills/hr/year-end-tax/calculators/tests
```

**Step 2: Python 패키지 초기화**

```bash
touch skills/hr/year-end-tax/calculators/__init__.py
touch skills/hr/year-end-tax/calculators/tests/__init__.py
```

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/
git commit -m "chore: scaffold year-end-tax skill directory structure"
```

---

## Phase 2: PDF 추출 및 레퍼런스 생성

> **중요:** 각 Task에서 PDF 텍스트를 추출할 때 `pdftotext` 로 해당 페이지 범위만 추출합니다.
> 추출 후 반드시 원문의 수치/조건/예외를 빠짐없이 정리하고, 모든 항목에 `[p.XX]` 출처를 기재합니다.

### Task 2: ref/10-tax-rates.md - 세율표/계산 기준 추출

> 세율표는 다른 계산기들의 기초이므로 가장 먼저 추출합니다.

**Files:**
- Create: `skills/hr/year-end-tax/ref/10-tax-rates.md`

**Step 1: PDF에서 세율 관련 텍스트 추출**

```bash
pdftotext -f 94 -l 95 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
pdftotext -f 162 -l 163 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출된 내용에서 다음을 정리:
- 근로소득공제 계산식 및 구간표
- 종합소득세율표 (과세표준 구간별 세율, 누진공제)
- 근로소득세액공제 계산식 및 한도
- 산출세액 계산 흐름

포맷:
```markdown
# 세율표 및 세액계산 기준 [ref: p.94, p.162-163]

## 근로소득공제 [p.94]
| 총급여액 | 공제액 |
|---------|--------|
| ... | ... |

## 종합소득세율 [p.XX]
| 과세표준 | 세율 | 누진공제 |
|---------|------|---------|
| ... | ... | ... |

## 근로소득세액공제 [p.162]
- 산출세액 기준 공제율
- 한도액
```

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/10-tax-rates.md
git commit -m "docs: extract tax rates reference from PDF (p.94, p.162-163)"
```

### Task 3: ref/01-income-types.md - 근로소득 유형/비과세 추출

**Files:**
- Create: `skills/hr/year-end-tax/ref/01-income-types.md`

**Step 1: PDF 추출**

```bash
pdftotext -f 50 -l 79 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출 항목:
- 근로소득의 범위 (소법 §20)
- 비과세 근로소득 전체 목록 및 한도
- 일용근로소득 vs 일반근로소득 구분 기준
- 근로소득의 수입시기
- 근로소득 수입금액 계산법

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/01-income-types.md
git commit -m "docs: extract income types reference from PDF (p.50-79)"
```

### Task 4: ref/02-basic-deductions.md - 인적공제 추출

**Files:**
- Create: `skills/hr/year-end-tax/ref/02-basic-deductions.md`

**Step 1: PDF 추출**

```bash
pdftotext -f 94 -l 104 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출 항목:
- 근로소득공제 구간표
- 기본공제 대상자 (본인, 배우자, 부양가족) 요건 (나이, 소득)
- 추가공제 (경로우대, 장애인, 부녀자, 한부모)
- 연금보험료 공제 (국민연금 등)
- 각 공제별 금액

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/02-basic-deductions.md
git commit -m "docs: extract personal deductions reference from PDF (p.94-104)"
```

### Task 5: ref/03-insurance.md - 보험료 공제 추출

**Files:**
- Create: `skills/hr/year-end-tax/ref/03-insurance.md`

**Step 1: PDF 추출**

```bash
pdftotext -f 107 -l 107 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
pdftotext -f 169 -l 173 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출 항목:
- 국민건강보험료, 고용보험료 (소득공제)
- 보장성보험료 세액공제 (대상, 한도, 공제율)
- 장애인전용 보장성보험료
- 공제 대상자 범위 및 예외

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/03-insurance.md
git commit -m "docs: extract insurance deductions reference from PDF (p.107, p.169-173)"
```

### Task 6: ref/04-medical.md - 의료비 공제 추출

**Files:**
- Create: `skills/hr/year-end-tax/ref/04-medical.md`

**Step 1: PDF 추출**

```bash
pdftotext -f 173 -l 187 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출 항목:
- 공제 대상자 (본인, 기본공제대상자)
- 공제 대상 의료비 목록 및 제외 항목
- 총급여 3% 초과분 계산
- 본인/65세이상/장애인/난임 한도 (무제한)
- 그 외 대상자 한도 (연 700만원)
- 공제율 (15%, 난임 30%, 미숙아/선천성이상아 20%)
- 안경/콘택트렌즈 한도 (1인당 50만원)
- 산후조리원 한도 (200만원)

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/04-medical.md
git commit -m "docs: extract medical deductions reference from PDF (p.173-187)"
```

### Task 7: ref/05-education.md - 교육비 공제 추출

**Files:**
- Create: `skills/hr/year-end-tax/ref/05-education.md`

**Step 1: PDF 추출**

```bash
pdftotext -f 187 -l 195 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출 항목:
- 본인 교육비 (대학원, 직업능력개발훈련비 등 - 한도 없음)
- 취학전 아동 (어린이집, 유치원, 학원 - 1인당 300만원)
- 초중고 (1인당 300만원)
- 대학생 (1인당 900만원)
- 교복구입비 (1인당 50만원, 중고생)
- 체험학습비 (1인당 30만원)
- 장애인 특수교육비
- 공제율 (15%)
- 대상자 요건 및 제외 항목

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/05-education.md
git commit -m "docs: extract education deductions reference from PDF (p.187-195)"
```

### Task 8: ref/06-housing.md - 주택 관련 공제 추출

**Files:**
- Create: `skills/hr/year-end-tax/ref/06-housing.md`

**Step 1: PDF 추출**

```bash
pdftotext -f 107 -l 119 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
pdftotext -f 122 -l 123 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
pdftotext -f 202 -l 204 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출 항목:
- 주택임차차입금 원리금상환액 공제 (전세자금 대출)
- 장기주택저당차입금 이자상환액 공제
- 주택마련저축 납입액 소득공제 (청약저축 등)
- 월세액 세액공제 (총급여 조건, 공제율, 한도)
- 각 항목별 무주택 요건, 주택 가액 기준

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/06-housing.md
git commit -m "docs: extract housing deductions reference from PDF (p.107-119, p.122-123, p.202-204)"
```

### Task 9: ref/07-donation.md - 기부금 공제 추출

**Files:**
- Create: `skills/hr/year-end-tax/ref/07-donation.md`

**Step 1: PDF 추출**

```bash
pdftotext -f 195 -l 201 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출 항목:
- 법정기부금 (한도, 공제율)
- 지정기부금 (종교단체/비종교단체 한도 차이, 공제율)
- 우리사주조합기부금
- 정치자금기부금 (세액공제율 차등)
- 이월공제 규정
- 공제율 (15%, 1천만원 초과분 30%)

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/07-donation.md
git commit -m "docs: extract donation deductions reference from PDF (p.195-201)"
```

### Task 10: ref/08-card-cash.md - 신용카드/현금영수증 공제 추출

**Files:**
- Create: `skills/hr/year-end-tax/ref/08-card-cash.md`

**Step 1: PDF 추출**

```bash
pdftotext -f 132 -l 147 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출 항목:
- 총급여 25% 초과분 계산
- 결제수단별 공제율 (신용카드 15%, 체크카드/현금영수증 30%)
- 전통시장/대중교통/문화비 추가공제율
- 총급여 구간별 공제한도
- 대상자 범위 및 제외 사용처
- 소득공제 종합한도 (조특법 §132의2)

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/08-card-cash.md
git commit -m "docs: extract card/cash deductions reference from PDF (p.132-147)"
```

### Task 11: ref/09-pension.md - 연금 관련 공제 추출

**Files:**
- Create: `skills/hr/year-end-tax/ref/09-pension.md`

**Step 1: PDF 추출**

```bash
pdftotext -f 103 -l 104 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
pdftotext -f 120 -l 121 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
pdftotext -f 164 -l 168 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출 항목:
- 연금보험료 소득공제 (국민연금, 공무원연금 등)
- 개인연금저축 소득공제 (구 조특법)
- 연금계좌 세액공제 (IRP, 연금저축)
  - 총급여 구간별 공제율 (12%/15%)
  - 납입한도 (연금저축 600만원, IRP 합산 900만원)
- 퇴직연금 추가납입 공제

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/09-pension.md
git commit -m "docs: extract pension deductions reference from PDF (p.103-104, p.120-121, p.164-168)"
```

### Task 12: ref/11-process-employer.md - 원천징수의무자 절차 추출

**Files:**
- Create: `skills/hr/year-end-tax/ref/11-process-employer.md`

**Step 1: PDF 추출**

```bash
pdftotext -f 27 -l 48 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출 항목:
- 연말정산 업무 일정 (월별 체크리스트)
- 서류제출 의무 사항
- 중점 확인사항
- 과다공제 주요 항목 및 가산세

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/11-process-employer.md
git commit -m "docs: extract employer process reference from PDF (p.27-48)"
```

### Task 13: ref/12-process-employee.md - 근로자 절차/일정 추출

**Files:**
- Create: `skills/hr/year-end-tax/ref/12-process-employee.md`

**Step 1: PDF 추출**

```bash
pdftotext -f 26 -l 26 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
pdftotext -f 358 -l 395 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: ref 파일 작성**

추출 항목:
- 간소화서비스 개편 내용 및 이용 방법
- 간소화자료 일괄제공 서비스
- 맞벌이 부부 연말정산 가이드
- 주요 용어 설명
- 첨부서류 목록

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/ref/12-process-employee.md
git commit -m "docs: extract employee process reference from PDF (p.26, p.358-395)"
```

---

## Phase 3: Python 계산기 개발 (TDD)

> **원칙:** 모든 계산기는 Phase 2에서 추출된 수학식을 기반으로 합니다.
> 3부 종합사례 (p.212-232)의 실제 계산 예시를 테스트 케이스로 활용합니다.

### Task 14: constants.py - 연도별 상수 정의

**Files:**
- Create: `skills/hr/year-end-tax/calculators/constants.py`

**Step 1: ref 파일들에서 모든 수치 상수를 수집하여 constants.py 작성**

ref 파일 전체를 읽고 다음 상수를 추출:
- 종합소득세율 구간 + 누진공제
- 근로소득공제 구간
- 각 공제별 한도액, 공제율
- 신용카드 등 공제율/한도

모든 상수에 `[ref: p.XX]` 출처 주석을 달 것.

**Step 2: 커밋**

```bash
git add skills/hr/year-end-tax/calculators/constants.py
git commit -m "feat: define year-end tax constants from PDF reference"
```

### Task 15: income_tax.py - 근로소득세 산출 계산기

**Files:**
- Create: `skills/hr/year-end-tax/calculators/tests/test_income_tax.py`
- Create: `skills/hr/year-end-tax/calculators/income_tax.py`

**Step 1: 3부 종합사례(p.212-232)에서 테스트 데이터 추출**

```bash
pdftotext -f 212 -l 232 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

종합사례의 실제 입력값과 결과값을 테스트 케이스로 사용.

**Step 2: 실패하는 테스트 작성**

```python
# tests/test_income_tax.py
from calculators.income_tax import (
    calculate_earned_income_deduction,
    calculate_tax_base,
    calculate_income_tax,
    calculate_earned_income_tax_credit,
)

def test_earned_income_deduction():
    """근로소득공제 계산 - 종합사례 기반"""
    # 종합사례의 총급여액과 근로소득공제 결과를 사용
    assert calculate_earned_income_deduction(total_salary) == expected_deduction

def test_income_tax_calculation():
    """과세표준 -> 산출세액 계산"""
    assert calculate_income_tax(tax_base) == expected_tax

def test_earned_income_tax_credit():
    """근로소득세액공제 계산"""
    assert calculate_earned_income_tax_credit(calculated_tax, total_salary) == expected_credit
```

**Step 3: 테스트 실행하여 실패 확인**

```bash
cd skills/hr/year-end-tax && python -m pytest calculators/tests/test_income_tax.py -v
```

Expected: FAIL

**Step 4: 최소 구현 작성**

ref/10-tax-rates.md와 constants.py 기반으로 구현.

**Step 5: 테스트 통과 확인**

```bash
cd skills/hr/year-end-tax && python -m pytest calculators/tests/test_income_tax.py -v
```

Expected: PASS

**Step 6: 커밋**

```bash
git add skills/hr/year-end-tax/calculators/income_tax.py skills/hr/year-end-tax/calculators/tests/test_income_tax.py
git commit -m "feat: implement income tax calculator with tests"
```

### Task 16: personal_deduction.py - 인적공제 계산기

**Files:**
- Create: `skills/hr/year-end-tax/calculators/tests/test_personal_deduction.py`
- Create: `skills/hr/year-end-tax/calculators/personal_deduction.py`

**Step 1: 실패하는 테스트 작성**

ref/02-basic-deductions.md 기반. 기본공제(1인 150만원), 추가공제(경로우대 100만원, 장애인 200만원, 부녀자 50만원, 한부모 100만원) 등 계산.

**Step 2: 테스트 실패 확인**
**Step 3: 최소 구현**
**Step 4: 테스트 통과 확인**
**Step 5: 커밋**

```bash
git add skills/hr/year-end-tax/calculators/personal_deduction.py skills/hr/year-end-tax/calculators/tests/test_personal_deduction.py
git commit -m "feat: implement personal deduction calculator with tests"
```

### Task 17: insurance_deduction.py - 보험료 공제 계산기

**Files:**
- Create: `skills/hr/year-end-tax/calculators/tests/test_insurance_deduction.py`
- Create: `skills/hr/year-end-tax/calculators/insurance_deduction.py`

**Step 1: 실패하는 테스트 (ref/03-insurance.md 기반)**
**Step 2: 테스트 실패 확인**
**Step 3: 최소 구현 (국민건강보험 소득공제 + 보장성보험 세액공제)**
**Step 4: 테스트 통과 확인**
**Step 5: 커밋**

```bash
git add skills/hr/year-end-tax/calculators/insurance_deduction.py skills/hr/year-end-tax/calculators/tests/test_insurance_deduction.py
git commit -m "feat: implement insurance deduction calculator with tests"
```

### Task 18: medical_deduction.py - 의료비 공제 계산기

**Files:**
- Create: `skills/hr/year-end-tax/calculators/tests/test_medical_deduction.py`
- Create: `skills/hr/year-end-tax/calculators/medical_deduction.py`

**Step 1: 실패하는 테스트 (ref/04-medical.md 기반)**

테스트 케이스:
- 총급여 3% 초과분 계산
- 본인/65세이상/장애인 (한도 없음)
- 난임시술비 30% 공제율
- 일반 대상자 700만원 한도
- 안경/콘택트렌즈 50만원 한도
- 산후조리원 200만원 한도 (총급여 7천만원 이하)

**Step 2: 테스트 실패 확인**
**Step 3: 최소 구현**
**Step 4: 테스트 통과 확인**
**Step 5: 커밋**

```bash
git add skills/hr/year-end-tax/calculators/medical_deduction.py skills/hr/year-end-tax/calculators/tests/test_medical_deduction.py
git commit -m "feat: implement medical deduction calculator with tests"
```

### Task 19: education_deduction.py - 교육비 공제 계산기

**Files:**
- Create: `skills/hr/year-end-tax/calculators/tests/test_education_deduction.py`
- Create: `skills/hr/year-end-tax/calculators/education_deduction.py`

**Step 1: 실패하는 테스트 (ref/05-education.md 기반)**

테스트 케이스:
- 본인 교육비 (한도 없음)
- 취학전 아동 (1인당 300만원)
- 초중고 (1인당 300만원) + 교복비 50만원 + 체험학습비 30만원
- 대학생 (1인당 900만원)
- 장애인 특수교육비 (한도 없음)
- 공제율 15%

**Step 2-5: TDD 사이클**
**Step 6: 커밋**

```bash
git add skills/hr/year-end-tax/calculators/education_deduction.py skills/hr/year-end-tax/calculators/tests/test_education_deduction.py
git commit -m "feat: implement education deduction calculator with tests"
```

### Task 20: housing_deduction.py - 주택 관련 공제 계산기

**Files:**
- Create: `skills/hr/year-end-tax/calculators/tests/test_housing_deduction.py`
- Create: `skills/hr/year-end-tax/calculators/housing_deduction.py`

**Step 1: 실패하는 테스트 (ref/06-housing.md 기반)**

테스트 케이스:
- 주택임차차입금 원리금상환액 소득공제
- 장기주택저당차입금 이자상환액 소득공제 (상환기간/고정금리 조건별)
- 주택마련저축 납입액 소득공제
- 월세액 세액공제 (총급여 조건별 공제율)

**Step 2-5: TDD 사이클**
**Step 6: 커밋**

```bash
git add skills/hr/year-end-tax/calculators/housing_deduction.py skills/hr/year-end-tax/calculators/tests/test_housing_deduction.py
git commit -m "feat: implement housing deduction calculator with tests"
```

### Task 21: donation_deduction.py - 기부금 공제 계산기

**Files:**
- Create: `skills/hr/year-end-tax/calculators/tests/test_donation_deduction.py`
- Create: `skills/hr/year-end-tax/calculators/donation_deduction.py`

**Step 1: 실패하는 테스트 (ref/07-donation.md 기반)**

테스트 케이스:
- 정치자금기부금 세액공제 (10만원 이하 100/110, 초과분 15%/25%)
- 법정기부금 (근로소득금액 100% 한도, 15%/30%)
- 우리사주조합기부금 (근로소득금액 30% 한도)
- 지정기부금 - 종교단체 (근로소득금액 10% 한도)
- 지정기부금 - 비종교 (근로소득금액 30% 한도)

**Step 2-5: TDD 사이클**
**Step 6: 커밋**

```bash
git add skills/hr/year-end-tax/calculators/donation_deduction.py skills/hr/year-end-tax/calculators/tests/test_donation_deduction.py
git commit -m "feat: implement donation deduction calculator with tests"
```

### Task 22: card_deduction.py - 신용카드/현금영수증 공제 계산기

**Files:**
- Create: `skills/hr/year-end-tax/calculators/tests/test_card_deduction.py`
- Create: `skills/hr/year-end-tax/calculators/card_deduction.py`

**Step 1: 실패하는 테스트 (ref/08-card-cash.md 기반)**

테스트 케이스:
- 총급여 25% 최저사용액 계산
- 결제수단별 공제율 적용 (신용카드 15%, 체크/현금 30%, 전통시장 40%, 대중교통 40%, 문화비 30%)
- 총급여 구간별 공제한도 적용
- 추가공제 한도 (전통시장, 대중교통, 문화비 각 100만원 추가)

**Step 2-5: TDD 사이클**
**Step 6: 커밋**

```bash
git add skills/hr/year-end-tax/calculators/card_deduction.py skills/hr/year-end-tax/calculators/tests/test_card_deduction.py
git commit -m "feat: implement card/cash deduction calculator with tests"
```

### Task 23: pension_deduction.py - 연금 공제 계산기

**Files:**
- Create: `skills/hr/year-end-tax/calculators/tests/test_pension_deduction.py`
- Create: `skills/hr/year-end-tax/calculators/pension_deduction.py`

**Step 1: 실패하는 테스트 (ref/09-pension.md 기반)**

테스트 케이스:
- 연금보험료 소득공제 (국민연금 전액 공제)
- 개인연금저축 소득공제 (연 72만원 한도)
- 연금계좌 세액공제 (연금저축+IRP 한도, 총급여 구간별 공제율)

**Step 2-5: TDD 사이클**
**Step 6: 커밋**

```bash
git add skills/hr/year-end-tax/calculators/pension_deduction.py skills/hr/year-end-tax/calculators/tests/test_pension_deduction.py
git commit -m "feat: implement pension deduction calculator with tests"
```

### Task 24: total_calculator.py - 통합 세액 계산기

**Files:**
- Create: `skills/hr/year-end-tax/calculators/tests/test_total_calculator.py`
- Create: `skills/hr/year-end-tax/calculators/total_calculator.py`

**Step 1: 3부 종합사례(p.212-232)에서 전체 흐름 테스트 데이터 추출**

```bash
pdftotext -f 212 -l 232 "docs/ref/2025년 원천징수의무자를 위한 연말정산 신고안내.pdf" - 2>/dev/null
```

**Step 2: End-to-End 실패하는 테스트 작성**

종합사례의 전체 입력값 -> 최종 환급/추가납부 세액까지의 흐름을 테스트.
모든 개별 calculator를 조합하여 총 급여 -> 과세표준 -> 산출세액 -> 세액공제 -> 결정세액 -> 기납부세액 차감 -> 환급/추가납부 계산.

**Step 3: 테스트 실패 확인**
**Step 4: 통합 계산 함수 구현**
**Step 5: 테스트 통과 확인**
**Step 6: 커밋**

```bash
git add skills/hr/year-end-tax/calculators/total_calculator.py skills/hr/year-end-tax/calculators/tests/test_total_calculator.py
git commit -m "feat: implement total tax calculator with end-to-end tests"
```

---

## Phase 4: SKILL.md 작성

### Task 25: SKILL.md 메인 스킬 파일 작성

**Files:**
- Create: `skills/hr/year-end-tax/SKILL.md`

**Step 1: SKILL.md 작성**

설계서(design doc)의 섹션 2, 3, 4를 기반으로:
- frontmatter (name, description, allowed-tools)
- 모드 선택 로직 (전체 점검 / 특정 항목 문의)
- 라우팅 인덱스 (주제 -> ref 파일 -> calculator 매핑)
- 위자드 모드 진행 순서
- 동작 규칙 (출처 표기, 확신도 표기, calculator 실행)
- 사용자 유형별 분기 (담당자/근로자)

**Step 2: 커밋**

```bash
git add skills/hr/year-end-tax/SKILL.md
git commit -m "feat: create year-end-tax SKILL.md with routing and Q&A logic"
```

---

## Phase 5: 검증 및 문서화

### Task 26: COVERAGE.md - 커버리지 검증 문서 생성

**Files:**
- Create: `skills/hr/year-end-tax/COVERAGE.md`

**Step 1: PDF 목차 전체를 순회하며 각 장/절이 어떤 ref 파일에 반영되었는지 매핑**

커버리지 표 작성:
- 레퍼런스 커버리지: PDF 장/절 -> ref 파일 -> 반영 상태
- 계산식 커버리지: 계산 항목 -> PDF 위치 -> 스크립트 -> 테스트 결과
- 미반영 항목: 의도적 제외 사항 + 사유

**Step 2: 모든 테스트 실행하여 결과 기록**

```bash
cd skills/hr/year-end-tax && python -m pytest calculators/tests/ -v --tb=short
```

**Step 3: 커밋**

```bash
git add skills/hr/year-end-tax/COVERAGE.md
git commit -m "docs: create coverage verification document"
```

### Task 27: UPDATE-GUIDE.md - PDF 갱신 절차서 작성

**Files:**
- Create: `skills/hr/year-end-tax/UPDATE-GUIDE.md`

**Step 1: 설계서 섹션 6의 갱신 워크플로우를 상세 절차서로 확장**

포함 내용:
- 새 PDF 수령 후 단계별 작업 절차
- pdftotext 사용법
- ref 파일 갱신 방법 (페이지 번호 재매핑)
- constants.py 업데이트 체크리스트
- 테스트 실행 및 검증 방법
- COVERAGE.md 재생성 방법

**Step 2: 커밋**

```bash
git add skills/hr/year-end-tax/UPDATE-GUIDE.md
git commit -m "docs: create PDF update guide"
```

### Task 28: README.md - 스킬 사용 설명서

**Files:**
- Create: `skills/hr/year-end-tax/README.md`

**Step 1: 스킬 개요, 사용법, 디렉토리 구조 설명 작성**

**Step 2: 커밋**

```bash
git add skills/hr/year-end-tax/README.md
git commit -m "docs: create year-end-tax skill README"
```

### Task 29: 최종 전체 테스트 및 리뷰

**Step 1: 전체 테스트 실행**

```bash
cd skills/hr/year-end-tax && python -m pytest calculators/tests/ -v --tb=long
```

**Step 2: COVERAGE.md 최종 업데이트 (테스트 결과 반영)**

**Step 3: 전체 ref 파일 vs PDF 원문 교차 검증 항목 최종 점검**

**Step 4: 최종 커밋**

```bash
git add -A skills/hr/year-end-tax/
git commit -m "feat: complete year-end-tax skill v1.0"
```

---

## 요약

| Phase | Task 수 | 내용 |
|-------|---------|------|
| Phase 1: 셋업 | 1 | 디렉토리 구조 |
| Phase 2: PDF 추출 | 12 | ref 파일 12개 생성 |
| Phase 3: 계산기 | 11 | constants + 9 calculators + total |
| Phase 4: SKILL.md | 1 | 메인 스킬 파일 |
| Phase 5: 검증/문서 | 4 | COVERAGE, UPDATE-GUIDE, README, 최종 검증 |
| **합계** | **29** | |
