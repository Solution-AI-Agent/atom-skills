"""
기부금 세액공제 계산기 [p.186-198]

정치자금, 고향사랑, 특례, 우리사주, 일반(종교외/종교) 기부금에 대한
세액공제를 계산합니다. 각 유형별 한도와 공제율이 다릅니다.
"""
from constants import (
    DONATION_POLITICAL_RATE_UNDER_100K,
    DONATION_POLITICAL_RATE_UNDER_30M,
    DONATION_POLITICAL_RATE_OVER_30M,
    DONATION_POLITICAL_THRESHOLD_1,
    DONATION_POLITICAL_THRESHOLD_2,
    DONATION_HOMETOWN_RATE_UNDER_100K,
    DONATION_HOMETOWN_RATE_OVER_100K,
    DONATION_SPECIAL_RATE_UNDER_10M,
    DONATION_SPECIAL_RATE_OVER_10M,
    DONATION_SPECIAL_THRESHOLD,
    DONATION_ESOP_LIMIT_RATE,
    DONATION_GENERAL_LIMIT_RATE_RELIGIOUS,
    DONATION_GENERAL_LIMIT_RATE_NON_RELIGIOUS,
    DONATION_GENERAL_LIMIT_RATE_NON_RELIGIOUS_WITH_RELIGIOUS,
)


def _calc_political_credit(amount: int) -> int:
    """정치자금기부금 세액공제 계산.

    - 10만원 이하: 100/110
    - 10만원 초과 3천만원 이하: 15%
    - 3천만원 초과: 25%

    Args:
        amount: 정치자금기부금 (원)

    Returns:
        세액공제 금액 (원)
    """
    if amount <= 0:
        return 0

    credit = 0

    tier_1 = min(amount, DONATION_POLITICAL_THRESHOLD_1)
    credit += tier_1 * DONATION_POLITICAL_RATE_UNDER_100K

    if amount > DONATION_POLITICAL_THRESHOLD_1:
        tier_2 = min(
            amount - DONATION_POLITICAL_THRESHOLD_1,
            DONATION_POLITICAL_THRESHOLD_2 - DONATION_POLITICAL_THRESHOLD_1,
        )
        credit += tier_2 * DONATION_POLITICAL_RATE_UNDER_30M

    if amount > DONATION_POLITICAL_THRESHOLD_2:
        tier_3 = amount - DONATION_POLITICAL_THRESHOLD_2
        credit += tier_3 * DONATION_POLITICAL_RATE_OVER_30M

    return int(credit)


def _calc_hometown_credit(amount: int) -> int:
    """고향사랑기부금 세액공제 계산.

    - 10만원 이하: 100/110
    - 10만원 초과: 15%

    Args:
        amount: 고향사랑기부금 (원)

    Returns:
        세액공제 금액 (원)
    """
    if amount <= 0:
        return 0

    credit = 0

    tier_1 = min(amount, DONATION_POLITICAL_THRESHOLD_1)
    credit += tier_1 * DONATION_HOMETOWN_RATE_UNDER_100K

    if amount > DONATION_POLITICAL_THRESHOLD_1:
        tier_2 = amount - DONATION_POLITICAL_THRESHOLD_1
        credit += tier_2 * DONATION_HOMETOWN_RATE_OVER_100K

    return int(credit)


def _calc_standard_credit(amount: int) -> int:
    """특례/우리사주/일반 기부금 세액공제 계산 (공통 로직).

    - 1천만원 이하: 15%
    - 1천만원 초과: 30%

    Args:
        amount: 기부금 (원)

    Returns:
        세액공제 금액 (원)
    """
    if amount <= 0:
        return 0

    tier_1 = min(amount, DONATION_SPECIAL_THRESHOLD)
    credit = tier_1 * DONATION_SPECIAL_RATE_UNDER_10M

    if amount > DONATION_SPECIAL_THRESHOLD:
        tier_2 = amount - DONATION_SPECIAL_THRESHOLD
        credit += tier_2 * DONATION_SPECIAL_RATE_OVER_10M

    return int(credit)


def calc_donation_tax_credit(
    earned_income_amount: int,
    political: int = 0,
    hometown: int = 0,
    special: int = 0,
    esop: int = 0,
    general_non_religious: int = 0,
    general_religious: int = 0,
) -> int:
    """기부금 세액공제 [p.186-198].

    공제 순서: 정치자금 -> 고향사랑 -> 특례 -> 우리사주 -> 종교외일반 -> 종교일반
    각 유형별로 근로소득금액에 따른 한도가 적용됩니다.

    Args:
        earned_income_amount: 근로소득금액 (원)
        political: 정치자금기부금 (원)
        hometown: 고향사랑기부금 (원)
        special: 특례기부금 (원)
        esop: 우리사주조합기부금 (원)
        general_non_religious: 일반기부금 - 종교단체 외 (원)
        general_religious: 일반기부금 - 종교단체 (원)

    Returns:
        세액공제 금액 (원)
    """
    if earned_income_amount <= 0:
        return 0

    total_credit = 0
    remaining = earned_income_amount

    # 1. 정치자금기부금: 한도 = 근로소득금액 x 100%
    political_limit = remaining
    political_eligible = min(political, political_limit)
    total_credit += _calc_political_credit(political_eligible)
    remaining -= political_eligible

    # 2. 고향사랑기부금: 한도 = (근로소득금액 - 정치자금) x 100%
    hometown_limit = remaining
    hometown_eligible = min(hometown, hometown_limit)
    total_credit += _calc_hometown_credit(hometown_eligible)
    remaining -= hometown_eligible

    # 3. 특례기부금: 한도 = (근로소득금액 - 정치자금 - 고향사랑) x 100%
    special_limit = remaining
    special_eligible = min(special, special_limit)
    total_credit += _calc_standard_credit(special_eligible)
    remaining -= special_eligible

    # 4. 우리사주조합기부금: 한도 = (잔여) x 30%
    esop_limit = int(remaining * DONATION_ESOP_LIMIT_RATE)
    esop_eligible = min(esop, esop_limit)
    total_credit += _calc_standard_credit(esop_eligible)
    remaining -= esop_eligible

    # 5. 일반기부금(종교외): 종교 있으면 잔여 x 20%, 없으면 잔여 x 30%
    has_religious = general_religious > 0
    non_religious_rate = DONATION_GENERAL_LIMIT_RATE_NON_RELIGIOUS_WITH_RELIGIOUS if has_religious else DONATION_GENERAL_LIMIT_RATE_NON_RELIGIOUS
    non_religious_limit = int(remaining * non_religious_rate)
    non_religious_eligible = min(general_non_religious, non_religious_limit)
    total_credit += _calc_standard_credit(non_religious_eligible)

    # 6. 일반기부금(종교): 잔여 x 10%
    religious_limit = int(remaining * DONATION_GENERAL_LIMIT_RATE_RELIGIOUS)
    religious_eligible = min(general_religious, religious_limit)
    total_credit += _calc_standard_credit(religious_eligible)

    return total_credit
