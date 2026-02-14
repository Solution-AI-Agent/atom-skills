"""
보험료 공제 계산기 [p.106-107, p.169-172]

소득공제: 국민건강보험료, 노인장기요양보험료, 고용보험료 (전액 공제)
세액공제: 보장성보험료 (12%), 장애인전용보장성보험료 (15%)
"""
from constants import (
    INSURANCE_DEDUCTION_LIMIT,
    INSURANCE_DEDUCTION_RATE,
    INSURANCE_DISABLED_DEDUCTION_LIMIT,
    INSURANCE_DISABLED_DEDUCTION_RATE,
)


def calc_insurance_income_deduction(
    health_insurance: int,
    long_term_care: int,
    employment_insurance: int = 0,
) -> int:
    """보험료 소득공제: 국민건강보험료 등 전액 공제 [p.104].

    Args:
        health_insurance: 국민건강보험료 (원)
        long_term_care: 노인장기요양보험료 (원)
        employment_insurance: 고용보험료 (원, 기본값 0)

    Returns:
        소득공제 금액 (원) - 전액 합산, 한도 없음
    """
    return health_insurance + long_term_care + employment_insurance


def calc_insurance_tax_credit(
    protection_premium: int,
    disabled_protection_premium: int = 0,
) -> int:
    """보장성보험료 세액공제 [p.170].

    보장성보험료와 장애인전용보장성보험료는 각각 별도의 100만원 한도가 적용됩니다.

    Args:
        protection_premium: 보장성보험료 납입액 (원)
        disabled_protection_premium: 장애인전용 보장성보험료 납입액 (원, 기본값 0)

    Returns:
        세액공제 금액 (원)
    """
    protection_eligible = min(protection_premium, INSURANCE_DEDUCTION_LIMIT)
    disabled_eligible = min(disabled_protection_premium, INSURANCE_DISABLED_DEDUCTION_LIMIT)

    protection_credit = int(protection_eligible * INSURANCE_DEDUCTION_RATE)
    disabled_credit = int(disabled_eligible * INSURANCE_DISABLED_DEDUCTION_RATE)

    return protection_credit + disabled_credit
