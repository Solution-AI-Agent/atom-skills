"""
신용카드 등 소득공제 계산기 (조특법 제126조의2) [p.131-147]

순수 함수로 구현. 모든 금액 단위: 원 (KRW).
"""
from constants import (
    CARD_MINIMUM_USAGE_RATE,
    CARD_RATE_CREDIT,
    CARD_RATE_DEBIT,
    CARD_RATE_CULTURE,
    CARD_RATE_TRADITIONAL,
    CARD_RATE_TRANSIT,
    CARD_LIMIT_UNDER_70M_RATE,
    CARD_LIMIT_UNDER_70M_CAP,
    CARD_LIMIT_OVER_70M,
    CARD_ADDITIONAL_LIMIT_UNDER_70M,
    CARD_ADDITIONAL_LIMIT_OVER_70M,
    CARD_SALARY_THRESHOLD,
)


def calc_card_deduction(
    total_salary: int,
    credit_card: int,
    debit_cash: int,
    culture: int = 0,
    traditional: int = 0,
    transit: int = 0,
) -> int:
    """신용카드 등 소득공제 [p.131-147]

    Args:
        total_salary: 총급여액
        credit_card: 신용카드 사용액 (대중교통/전통시장/문화체육 제외분)
        debit_cash: 체크카드+현금영수증 사용액 (대중교통/전통시장/문화체육 제외분)
        culture: 문화체육 사용분 (총급여 7천만원 이하만 적용)
        traditional: 전통시장 사용분
        transit: 대중교통 이용분

    Returns:
        소득공제 금액 (원, 정수)

    계산 과정:
        1. 최저사용금액 = total_salary x 25%
        2. 총 사용액이 최저사용금액 미만이면 공제 0원
        3. 결제수단별 공제율 적용 (신용카드부터 최저사용금액 차감)
        4. 기본 공제 한도 적용
        5. 추가 공제 (문화체육+전통시장+대중교통) 한도 적용
    """
    minimum_usage = int(total_salary * CARD_MINIMUM_USAGE_RATE)

    effective_culture = culture if total_salary <= CARD_SALARY_THRESHOLD else 0

    categories = _build_categories(
        credit_card, debit_cash, effective_culture, traditional, transit,
    )

    total_usage = sum(amount for amount, _ in categories)
    if total_usage <= minimum_usage:
        return 0

    net_deductions = _calc_net_deductions(categories, minimum_usage)
    net_total = sum(net_deductions)

    if net_total <= 0:
        return 0

    basic_limit = _calc_basic_limit(total_salary)
    basic_deduction = min(net_total, basic_limit)

    additional_deduction = _calc_additional_deduction(
        net_total, basic_limit, net_deductions, total_salary,
    )

    return int(basic_deduction + additional_deduction)


def _build_categories(
    credit_card: int,
    debit_cash: int,
    culture: int,
    traditional: int,
    transit: int,
) -> list[tuple[int, float]]:
    """결제수단별 (사용액, 공제율) 목록 생성.

    최저사용금액 차감 순서: 신용카드 -> 체크카드/현금 -> 문화체육 -> 전통시장 -> 대중교통
    """
    return [
        (credit_card, CARD_RATE_CREDIT),
        (debit_cash, CARD_RATE_DEBIT),
        (culture, CARD_RATE_CULTURE),
        (traditional, CARD_RATE_TRADITIONAL),
        (transit, CARD_RATE_TRANSIT),
    ]


def _calc_net_deductions(
    categories: list[tuple[int, float]],
    minimum_usage: int,
) -> list[float]:
    """각 카테고리별 최저사용금액 차감 후 순 공제액 계산.

    최저사용금액을 신용카드부터 순서대로 차감합니다.
    """
    min_remaining = minimum_usage
    net_deductions = []

    for amount, rate in categories:
        consumed = min(amount, min_remaining)
        net_amount = amount - consumed
        net_deduction = net_amount * rate
        net_deductions.append(net_deduction)
        min_remaining -= consumed

    return net_deductions


def _calc_basic_limit(total_salary: int) -> int:
    """기본 공제 한도 계산.

    - 총급여 7천만원 이하: min(총급여x20%, 300만원)
    - 총급여 7천만원 초과: 250만원
    """
    if total_salary <= CARD_SALARY_THRESHOLD:
        return min(
            int(total_salary * CARD_LIMIT_UNDER_70M_RATE),
            CARD_LIMIT_UNDER_70M_CAP,
        )
    return CARD_LIMIT_OVER_70M


def _calc_additional_deduction(
    net_total: float,
    basic_limit: int,
    net_deductions: list[float],
    total_salary: int,
) -> int:
    """추가 공제 계산 (문화체육 + 전통시장 + 대중교통).

    기본 한도 초과시, 추가 공제 카테고리의 순공제액 합계와
    추가 한도 중 작은 금액을 적용합니다.
    """
    excess = net_total - basic_limit
    if excess <= 0:
        return 0

    # net_deductions 인덱스: [0]=신용카드, [1]=체크/현금, [2]=문화, [3]=전통, [4]=대중교통
    additional_sources = net_deductions[2] + net_deductions[3] + net_deductions[4]

    if total_salary <= CARD_SALARY_THRESHOLD:
        additional_limit = CARD_ADDITIONAL_LIMIT_UNDER_70M
    else:
        additional_limit = CARD_ADDITIONAL_LIMIT_OVER_70M

    return int(min(excess, additional_sources, additional_limit))
