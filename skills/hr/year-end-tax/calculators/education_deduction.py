"""
교육비 세액공제 계산기 [p.177-186]

본인, 취학전 아동, 초중고, 대학생, 장애인 특수교육비에 대한
세액공제를 계산합니다. 공제율 15%.
"""
from constants import (
    EDUCATION_RATE,
    EDUCATION_LIMIT_PRESCHOOL,
    EDUCATION_LIMIT_ELEMENTARY_MIDDLE_HIGH,
    EDUCATION_LIMIT_UNIVERSITY,
)


def _cap_per_person(amounts: list[int], limit: int) -> int:
    """각 개인별로 한도를 적용한 후 합산합니다.

    Args:
        amounts: 각 개인별 교육비 리스트 (원)
        limit: 1인당 한도 (원)

    Returns:
        한도 적용 후 합산 금액 (원)
    """
    return sum(min(amount, limit) for amount in amounts)


def calc_education_tax_credit(
    self_education: int = 0,
    preschool_amounts: list[int] | None = None,
    school_amounts: list[int] | None = None,
    university_amounts: list[int] | None = None,
    disabled_special: int = 0,
) -> int:
    """교육비 세액공제 [p.177-186].

    본인 교육비와 장애인 특수교육비는 한도 없이 전액 공제 대상.
    취학전/초중고/대학생은 각각 1인당 한도가 있으며, 개인별로 한도를 적용합니다.
    모든 공제 대상 금액의 합계에 15%를 곱하여 세액공제를 산출합니다.

    Args:
        self_education: 본인 교육비 (원, 한도 없음)
        preschool_amounts: 취학전 아동별 교육비 리스트 (원, 1인당 300만원 한도)
        school_amounts: 초중고 학생별 교육비 리스트 (원, 1인당 300만원 한도)
        university_amounts: 대학생별 교육비 리스트 (원, 1인당 900만원 한도)
        disabled_special: 장애인 특수교육비 (원, 한도 없음)

    Returns:
        세액공제 금액 (원)
    """
    preschool_total = (
        _cap_per_person(preschool_amounts, EDUCATION_LIMIT_PRESCHOOL)
        if preschool_amounts
        else 0
    )

    school_total = (
        _cap_per_person(school_amounts, EDUCATION_LIMIT_ELEMENTARY_MIDDLE_HIGH)
        if school_amounts
        else 0
    )

    university_total = (
        _cap_per_person(university_amounts, EDUCATION_LIMIT_UNIVERSITY)
        if university_amounts
        else 0
    )

    total_eligible = (
        self_education
        + preschool_total
        + school_total
        + university_total
        + disabled_special
    )

    return int(total_eligible * EDUCATION_RATE)
