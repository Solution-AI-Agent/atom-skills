"""
근로소득공제 + 산출세액 + 근로소득세액공제 계산기

2025 귀속 연말정산. 모든 금액 단위: 원 (KRW).
Pure functions, no side effects.

References:
  - 근로소득공제: 소법 제47조 [p.94]
  - 산출세액: 소법 제55조 [p.83]
  - 근로소득세액공제: 소법 제59조 [p.162-163]
"""

from constants import (
    EARNED_INCOME_DEDUCTION_BRACKETS,
    EARNED_INCOME_DEDUCTION_CAP,
    INCOME_TAX_BRACKETS,
    EARNED_INCOME_TAX_CREDIT_THRESHOLD,
    EARNED_INCOME_TAX_CREDIT_RATE_LOW,
    EARNED_INCOME_TAX_CREDIT_BASE,
    EARNED_INCOME_TAX_CREDIT_RATE_HIGH,
    EARNED_INCOME_TAX_CREDIT_LIMITS,
    EARNED_INCOME_TAX_CREDIT_MIN_LIMIT,
)


def calc_earned_income_deduction(total_salary: int) -> int:
    """근로소득공제 계산 [p.94]

    총급여액에 구간별 공제율을 적용하여 근로소득공제액을 산출한다.
    공제한도: 2,000만원.

    Args:
        total_salary: 총급여액 (원)

    Returns:
        근로소득공제액 (원)
    """
    if total_salary <= 0:
        return 0

    prev_upper = 0
    for upper, base_deduction, rate in EARNED_INCOME_DEDUCTION_BRACKETS:
        if total_salary <= upper:
            deduction = base_deduction + int((total_salary - prev_upper) * rate)
            return min(deduction, EARNED_INCOME_DEDUCTION_CAP)
        prev_upper = upper

    return EARNED_INCOME_DEDUCTION_CAP


def calc_earned_income_amount(total_salary: int) -> int:
    """근로소득금액 = 총급여액 - 근로소득공제 [p.94]

    Args:
        total_salary: 총급여액 (원)

    Returns:
        근로소득금액 (원)
    """
    return total_salary - calc_earned_income_deduction(total_salary)


def calc_taxable_income(earned_income_amount: int, total_deductions: int) -> int:
    """과세표준 = 근로소득금액 - 소득공제합계 [p.94]

    과세표준은 음수가 될 수 없다.

    Args:
        earned_income_amount: 근로소득금액 (원)
        total_deductions: 소득공제합계 (원)

    Returns:
        과세표준 (원), 최소 0
    """
    return max(0, earned_income_amount - total_deductions)


def calc_calculated_tax(taxable_income: int) -> int:
    """산출세액: 과세표준에 기본세율 적용 [p.83]

    세액 = 과세표준 x 세율 - 누진공제액

    Args:
        taxable_income: 과세표준 (원)

    Returns:
        산출세액 (원)
    """
    if taxable_income <= 0:
        return 0

    for upper, progressive_deduction, rate in INCOME_TAX_BRACKETS:
        if taxable_income <= upper:
            return int(taxable_income * rate - progressive_deduction)

    return 0


def calc_earned_income_tax_credit(calculated_tax: int, total_salary: int) -> int:
    """근로소득세액공제 [p.162-163]

    Step 1: 산출세액 기준 공제액 산출
      - 130만원 이하: 산출세액 x 55%
      - 130만원 초과: 71.5만원 + (산출세액 - 130만원) x 30%

    Step 2: 총급여액 구간별 한도 적용

    Args:
        calculated_tax: 산출세액 (원)
        total_salary: 총급여액 (원)

    Returns:
        근로소득세액공제액 (원)
    """
    if calculated_tax <= 0:
        return 0

    # Step 1: base credit
    if calculated_tax <= EARNED_INCOME_TAX_CREDIT_THRESHOLD:
        credit = int(calculated_tax * EARNED_INCOME_TAX_CREDIT_RATE_LOW)
    else:
        excess = calculated_tax - EARNED_INCOME_TAX_CREDIT_THRESHOLD
        credit = EARNED_INCOME_TAX_CREDIT_BASE + int(excess * EARNED_INCOME_TAX_CREDIT_RATE_HIGH)

    # Step 2: apply salary-based limit
    limit = _calc_credit_limit(total_salary)

    return min(credit, limit)


def _calc_credit_limit(total_salary: int) -> int:
    """총급여액 구간별 근로소득세액공제 한도 계산 [p.162]

    Args:
        total_salary: 총급여액 (원)

    Returns:
        세액공제 한도액 (원)
    """
    prev_upper = 0
    for upper, base_limit, decrease_rate, min_limit in EARNED_INCOME_TAX_CREDIT_LIMITS:
        if total_salary <= upper:
            decreased = int(base_limit - (total_salary - prev_upper) * decrease_rate)
            return max(decreased, min_limit)
        prev_upper = upper

    return EARNED_INCOME_TAX_CREDIT_MIN_LIMIT
