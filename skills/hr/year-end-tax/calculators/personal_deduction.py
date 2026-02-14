"""
인적공제 (기본/추가) + 자녀세액공제 계산기

2025 귀속 연말정산. 모든 금액 단위: 원 (KRW).
Pure functions, no side effects.

References:
  - 기본공제: 소법 제50조 [p.95]
  - 추가공제: 소법 제51조 [p.99-102]
  - 자녀세액공제: 소법 제59조의2 [p.160-161]
"""

from constants import (
    PERSONAL_DEDUCTION_PER_PERSON,
    ADDITIONAL_DEDUCTION_ELDERLY,
    ADDITIONAL_DEDUCTION_DISABLED,
    ADDITIONAL_DEDUCTION_SINGLE_PARENT,
    ADDITIONAL_DEDUCTION_WOMAN,
    CHILD_CREDIT_1,
    CHILD_CREDIT_2,
    CHILD_CREDIT_EXTRA,
    CHILD_CREDIT_BIRTH_1ST,
    CHILD_CREDIT_BIRTH_2ND,
    CHILD_CREDIT_BIRTH_3RD,
)


def calc_basic_personal_deduction(num_dependents: int) -> int:
    """기본공제 = 1인당 150만원 x 인원수 [p.95]

    본인, 배우자, 부양가족 중 소득요건을 충족하는 인원에 대해
    1인당 150만원을 공제한다.

    Args:
        num_dependents: 기본공제 대상 인원수 (본인 포함)

    Returns:
        기본공제액 (원)
    """
    return num_dependents * PERSONAL_DEDUCTION_PER_PERSON


def calc_additional_deduction(
    elderly_count: int = 0,
    disabled_count: int = 0,
    is_single_parent: bool = False,
    is_woman_deduction: bool = False,
) -> int:
    """추가공제 [p.99-102]

    - 경로우대: 70세 이상 1인당 100만원
    - 장애인: 1인당 200만원
    - 한부모: 100만원
    - 부녀자: 50만원
    - 한부모와 부녀자는 중복 적용 불가 (한부모 우선)

    Args:
        elderly_count: 경로우대 대상 인원수 (70세 이상)
        disabled_count: 장애인 인원수
        is_single_parent: 한부모 해당 여부
        is_woman_deduction: 부녀자 공제 해당 여부

    Returns:
        추가공제액 (원)
    """
    total = 0
    total += elderly_count * ADDITIONAL_DEDUCTION_ELDERLY
    total += disabled_count * ADDITIONAL_DEDUCTION_DISABLED

    # 한부모와 부녀자는 중복 적용 불가, 한부모 우선
    if is_single_parent:
        total += ADDITIONAL_DEDUCTION_SINGLE_PARENT
    elif is_woman_deduction:
        total += ADDITIONAL_DEDUCTION_WOMAN

    return total


def calc_child_tax_credit(
    children_over_8: int,
    birth_orders: list[int] | None = None,
) -> int:
    """자녀세액공제 [p.160-161]

    8세 이상 자녀:
      - 1명: 25만원
      - 2명: 55만원
      - 3명 이상: 55만원 + (인원-2) x 30만원

    출산/입양 자녀 (출생순위별):
      - 첫째: 30만원
      - 둘째: 50만원
      - 셋째 이상: 70만원

    Args:
        children_over_8: 8세 이상 기본공제 대상 자녀 수
        birth_orders: 해당 과세연도 출산/입양 자녀의 출생순위 리스트
                      (e.g., [3] for 셋째, [1, 2] for 첫째+둘째)

    Returns:
        자녀세액공제액 (원)
    """
    total = 0

    # 8세 이상 자녀 공제
    if children_over_8 == 1:
        total += CHILD_CREDIT_1
    elif children_over_8 == 2:
        total += CHILD_CREDIT_2
    elif children_over_8 >= 3:
        total += CHILD_CREDIT_2 + (children_over_8 - 2) * CHILD_CREDIT_EXTRA

    # 출산/입양 자녀 공제
    if birth_orders:
        for order in birth_orders:
            total += _birth_credit_by_order(order)

    return total


def _birth_credit_by_order(order: int) -> int:
    """출생순위별 출산/입양 세액공제액 [p.160]

    Args:
        order: 출생순위 (1=첫째, 2=둘째, 3이상=셋째이상)

    Returns:
        출산/입양 세액공제액 (원)
    """
    if order <= 1:
        return CHILD_CREDIT_BIRTH_1ST
    if order == 2:
        return CHILD_CREDIT_BIRTH_2ND
    return CHILD_CREDIT_BIRTH_3RD
