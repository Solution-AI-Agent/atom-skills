"""
주택자금 공제 계산기 [p.107-119, p.122-123, p.202-204]

주택임차차입금, 주택마련저축, 장기주택저당차입금 소득공제 및
월세액 세액공제를 계산합니다.
"""
from constants import (
    HOUSING_RENT_LOAN_RATE,
    HOUSING_RENT_LOAN_SAVINGS_LIMIT,
    HOUSING_SAVINGS_RATE,
    HOUSING_SAVINGS_ANNUAL_LIMIT,
    RENT_CREDIT_SALARY_LIMIT,
    RENT_CREDIT_ANNUAL_LIMIT,
    RENT_CREDIT_RATE_LOW,
    RENT_CREDIT_RATE_HIGH,
    RENT_CREDIT_SALARY_THRESHOLD,
)


def calc_housing_loan_deduction(
    rent_loan_repayment: int = 0,
    mortgage_interest: int = 0,
    housing_savings: int = 0,
    mortgage_limit: int = 20_000_000,
) -> int:
    """주택자금 소득공제 [p.107-119].

    주택임차차입금과 주택마련저축은 합산하여 400만원 한도가 적용됩니다.
    장기주택저당차입금은 별도 한도가 적용됩니다.

    Args:
        rent_loan_repayment: 주택임차차입금 원리금상환액 (원)
        mortgage_interest: 장기주택저당차입금 이자상환액 (원)
        housing_savings: 주택마련저축 납입액 (원)
        mortgage_limit: 장기주택저당차입금 한도 (원, 상환기간/방식에 따라 다름)

    Returns:
        소득공제 금액 (원)
    """
    # 주택임차차입금: 원리금상환액 x 40%
    rent_loan_deduction = int(rent_loan_repayment * HOUSING_RENT_LOAN_RATE)

    # 주택마련저축: 납입액(300만원 한도) x 40%
    savings_capped = min(housing_savings, HOUSING_SAVINGS_ANNUAL_LIMIT)
    savings_deduction = int(savings_capped * HOUSING_SAVINGS_RATE)

    # 주택임차 + 주택마련저축 합산 400만원 한도
    rent_savings_combined = min(
        rent_loan_deduction + savings_deduction,
        HOUSING_RENT_LOAN_SAVINGS_LIMIT,
    )

    # 장기주택저당차입금: 이자상환액 (한도 적용)
    mortgage_deduction = min(mortgage_interest, mortgage_limit)

    return rent_savings_combined + mortgage_deduction


def calc_rent_tax_credit(total_salary: int, annual_rent: int) -> int:
    """월세액 세액공제 [p.202-204].

    총급여 8천만원 이하인 경우에만 적용됩니다.
    연간 월세 1,000만원 한도 내에서 공제율을 적용합니다.

    Args:
        total_salary: 총급여액 (원)
        annual_rent: 연간 월세 합계 (원)

    Returns:
        세액공제 금액 (원)
    """
    if total_salary > RENT_CREDIT_SALARY_LIMIT:
        return 0

    rent_capped = min(annual_rent, RENT_CREDIT_ANNUAL_LIMIT)

    rate = (
        RENT_CREDIT_RATE_LOW
        if total_salary <= RENT_CREDIT_SALARY_THRESHOLD
        else RENT_CREDIT_RATE_HIGH
    )

    return int(rent_capped * rate)
