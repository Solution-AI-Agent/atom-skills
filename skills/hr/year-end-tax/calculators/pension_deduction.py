"""
연금 공제 계산기 [p.103-104, p.164-168]

소득공제: 국민연금 보험료 (전액 공제)
세액공제: 연금저축 + 퇴직연금 (한도 및 소득구간별 공제율 적용)
"""
from constants import (
    PENSION_RATE_HIGH_SALARY,
    PENSION_RATE_LOW_SALARY,
    PENSION_SALARY_THRESHOLD,
    PENSION_SAVINGS_LIMIT,
    PENSION_TOTAL_LIMIT,
)


def calc_pension_insurance_deduction(national_pension: int) -> int:
    """연금보험료 소득공제: 국민연금 전액 공제 [p.103].

    Args:
        national_pension: 국민연금 납입액 (원)

    Returns:
        소득공제 금액 (원) - 전액 공제, 한도 없음
    """
    return national_pension


def calc_pension_tax_credit(
    total_salary: int,
    pension_savings: int,
    retirement_pension: int = 0,
) -> int:
    """연금계좌 세액공제 [p.164].

    연금저축 한도: 600만원
    합산한도 (연금저축 + 퇴직연금): 900만원
    공제율: 총급여 5,500만원 이하 15%, 초과 12%

    Args:
        total_salary: 총급여액 (원)
        pension_savings: 연금저축 납입액 (원)
        retirement_pension: 퇴직연금 근로자부담금 (원, 기본값 0)

    Returns:
        세액공제 금액 (원)
    """
    savings_eligible = min(pension_savings, PENSION_SAVINGS_LIMIT)
    retirement_eligible = min(retirement_pension, PENSION_TOTAL_LIMIT - savings_eligible)
    total_eligible = savings_eligible + retirement_eligible

    rate = (
        PENSION_RATE_LOW_SALARY
        if total_salary <= PENSION_SALARY_THRESHOLD
        else PENSION_RATE_HIGH_SALARY
    )

    return int(total_eligible * rate)
