"""
통합 연말정산 계산기

2025 귀속 연말정산. 모든 금액 단위: 원 (KRW).
Pure functions, no side effects.

개별 계산기 모듈을 조합하여 연말정산 전체 과정을 수행합니다.

References:
  - 근로소득공제/산출세액/근로소득세액공제: income_tax.py
  - 인적공제/자녀세액공제: personal_deduction.py
  - 연금공제: pension_deduction.py
  - 소득공제 종합한도: 조특법 제132조의2 [p.147]
"""
from income_tax import (
    calc_earned_income_deduction,
    calc_earned_income_amount,
    calc_taxable_income,
    calc_calculated_tax,
    calc_earned_income_tax_credit,
)
from personal_deduction import (
    calc_basic_personal_deduction,
    calc_additional_deduction,
    calc_child_tax_credit,
)
from insurance_deduction import calc_insurance_income_deduction
from pension_deduction import (
    calc_pension_insurance_deduction,
    calc_pension_tax_credit,
)
from constants import TOTAL_DEDUCTION_LIMIT


def calc_year_end_tax(
    total_salary: int,
    # 인적공제
    num_dependents: int,
    elderly_count: int = 0,
    disabled_count: int = 0,
    is_single_parent: bool = False,
    is_woman_deduction: bool = False,
    # 소득공제
    national_pension: int = 0,
    health_insurance: int = 0,
    long_term_care: int = 0,
    employment_insurance: int = 0,
    housing_loan_deduction: int = 0,
    card_deduction: int = 0,
    other_income_deductions: int = 0,
    # 세액공제
    children_over_8: int = 0,
    birth_orders: list[int] | None = None,
    pension_savings: int = 0,
    retirement_pension: int = 0,
    insurance_tax_credit: int = 0,
    medical_tax_credit: int = 0,
    education_tax_credit: int = 0,
    donation_tax_credit: int = 0,
    other_tax_credits: int = 0,
    # 기납부
    prepaid_tax: int = 0,
) -> dict:
    """통합 연말정산 계산 [p.94, p.162]

    개별 계산기 모듈을 조합하여 총급여액부터 환급/추가납부까지
    연말정산 전체 과정을 수행합니다.

    Args:
        total_salary: 총급여액
        num_dependents: 기본공제 대상 인원 (본인 포함)
        elderly_count: 경로우대 대상 인원 (70세 이상)
        disabled_count: 장애인 인원
        is_single_parent: 한부모 해당 여부
        is_woman_deduction: 부녀자 공제 해당 여부
        national_pension: 국민연금 납입액
        health_insurance: 국민건강보험료
        long_term_care: 노인장기요양보험료
        employment_insurance: 고용보험료
        housing_loan_deduction: 주택자금 소득공제
        card_deduction: 신용카드등 소득공제 (calc_card_deduction으로 계산)
        other_income_deductions: 기타 소득공제
        children_over_8: 8세 이상 기본공제 대상 자녀 수
        birth_orders: 출산/입양 자녀 출생순위 리스트
        pension_savings: 연금저축 납입액
        retirement_pension: 퇴직연금 근로자부담금
        insurance_tax_credit: 보험료 세액공제 (사전 계산값)
        medical_tax_credit: 의료비 세액공제 (사전 계산값)
        education_tax_credit: 교육비 세액공제 (사전 계산값)
        donation_tax_credit: 기부금 세액공제 (사전 계산값)
        other_tax_credits: 기타 세액공제
        prepaid_tax: 기납부세액

    Returns:
        dict with all intermediate and final values
    """
    # Step 1: 근로소득공제 및 근로소득금액
    earned_income_deduction = calc_earned_income_deduction(total_salary)
    earned_income_amount = calc_earned_income_amount(total_salary)

    # Step 2: 인적공제
    basic_personal = calc_basic_personal_deduction(num_dependents)
    additional_personal = calc_additional_deduction(
        elderly_count=elderly_count,
        disabled_count=disabled_count,
        is_single_parent=is_single_parent,
        is_woman_deduction=is_woman_deduction,
    )
    personal_deduction = basic_personal + additional_personal

    # Step 3: 연금보험료 소득공제
    pension_insurance_deduction = calc_pension_insurance_deduction(national_pension)

    # Step 4: 보험료 소득공제 (건강보험 등)
    insurance_income_deduction = calc_insurance_income_deduction(
        health_insurance=health_insurance,
        long_term_care=long_term_care,
        employment_insurance=employment_insurance,
    )

    # Step 5: 소득공제 합계 (카드공제 및 기타 제외)
    total_income_deduction = (
        personal_deduction
        + pension_insurance_deduction
        + insurance_income_deduction
        + housing_loan_deduction
    )

    # Step 6: 소득공제 종합한도 적용 (카드 + 기타)
    limited_card_and_other = _apply_deduction_limit(
        card_deduction, other_income_deductions,
    )

    # Step 7: 과세표준
    total_deductions = total_income_deduction + limited_card_and_other
    taxable_income = calc_taxable_income(earned_income_amount, total_deductions)

    # Step 8: 산출세액
    calculated_tax = calc_calculated_tax(taxable_income)

    # Step 9: 세액공제
    earned_income_tax_credit = calc_earned_income_tax_credit(
        calculated_tax, total_salary,
    )

    child_tax_credit = calc_child_tax_credit(
        children_over_8=children_over_8,
        birth_orders=birth_orders,
    )

    pension_tax_credit = calc_pension_tax_credit(
        total_salary=total_salary,
        pension_savings=pension_savings,
        retirement_pension=retirement_pension,
    )

    special_tax_credit = (
        insurance_tax_credit
        + medical_tax_credit
        + education_tax_credit
        + donation_tax_credit
    )

    total_tax_credit = (
        earned_income_tax_credit
        + child_tax_credit
        + pension_tax_credit
        + special_tax_credit
        + other_tax_credits
    )

    # Step 10: 결정세액 (음수 불가)
    determined_tax = max(0, calculated_tax - total_tax_credit)

    # Step 11: 환급/추가납부
    refund_amount = determined_tax - prepaid_tax

    return {
        "total_salary": total_salary,
        "earned_income_deduction": earned_income_deduction,
        "earned_income_amount": earned_income_amount,
        "personal_deduction": personal_deduction,
        "pension_insurance_deduction": pension_insurance_deduction,
        "insurance_income_deduction": insurance_income_deduction,
        "housing_deduction": housing_loan_deduction,
        "card_deduction": card_deduction,
        "total_income_deduction": total_income_deduction,
        "taxable_income": taxable_income,
        "calculated_tax": calculated_tax,
        "earned_income_tax_credit": earned_income_tax_credit,
        "child_tax_credit": child_tax_credit,
        "pension_tax_credit": pension_tax_credit,
        "special_tax_credit": special_tax_credit,
        "total_tax_credit": total_tax_credit,
        "determined_tax": determined_tax,
        "prepaid_tax": prepaid_tax,
        "refund_amount": refund_amount,
    }


def _apply_deduction_limit(
    card_deduction: int,
    other_income_deductions: int,
) -> int:
    """소득공제 종합한도 적용 (조특법 제132조의2) [p.147]

    신용카드등 소득공제 + 기타 소득공제의 합계가
    종합한도(2,500만원)를 초과하지 않도록 제한합니다.

    Args:
        card_deduction: 신용카드등 소득공제
        other_income_deductions: 기타 소득공제

    Returns:
        한도 적용 후 합산 소득공제액
    """
    combined = card_deduction + other_income_deductions
    return min(combined, TOTAL_DEDUCTION_LIMIT)
