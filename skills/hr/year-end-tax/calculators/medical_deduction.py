"""
의료비 세액공제 계산기 [p.172-177]

총급여액의 3% 초과분에 대해 세액공제.
기준금액(threshold)은 낮은 우선순위 카테고리부터 차감:
  그 외 부양가족 -> 본인등 -> 미숙아 -> 난임시술비
"""
from constants import (
    MEDICAL_OTHER_DEPENDENT_LIMIT,
    MEDICAL_RATE_GENERAL,
    MEDICAL_RATE_INFERTILITY,
    MEDICAL_RATE_PREMATURE,
    MEDICAL_THRESHOLD_RATE,
)


def calc_medical_tax_credit(
    total_salary: int,
    other_dependent_medical: int,
    self_etc_medical: int,
    infertility_medical: int = 0,
    premature_medical: int = 0,
) -> int:
    """의료비 세액공제 [p.172-177].

    계산 순서:
    1. threshold = total_salary x 3%
    2. threshold를 우선순위 순서대로 차감 (그 외 부양가족 -> 본인등 -> 미숙아 -> 난임)
    3. 그 외 부양가족은 700만원 한도 적용
    4. 카테고리별 세율 적용: 일반 15%, 미숙아 20%, 난임 30%

    Args:
        total_salary: 총급여액 (원)
        other_dependent_medical: 그 외 부양가족 의료비 (원)
        self_etc_medical: 본인/장애인/65세이상/6세이하 의료비 (원)
        infertility_medical: 난임시술비 (원, 기본값 0)
        premature_medical: 미숙아/선천성이상아 의료비 (원, 기본값 0)

    Returns:
        세액공제 금액 (원)
    """
    threshold = int(total_salary * MEDICAL_THRESHOLD_RATE)

    remaining_threshold = threshold

    # 1. 그 외 부양가족에서 threshold 차감
    other_after_threshold = max(0, other_dependent_medical - remaining_threshold)
    remaining_threshold = max(0, remaining_threshold - other_dependent_medical)

    # 700만원 한도 적용
    other_eligible = min(other_after_threshold, MEDICAL_OTHER_DEPENDENT_LIMIT)

    # 2. 본인등에서 remaining threshold 차감
    self_after_threshold = max(0, self_etc_medical - remaining_threshold)
    remaining_threshold = max(0, remaining_threshold - self_etc_medical)

    self_eligible = self_after_threshold

    # 3. 미숙아에서 remaining threshold 차감
    premature_after_threshold = max(0, premature_medical - remaining_threshold)
    remaining_threshold = max(0, remaining_threshold - premature_medical)

    premature_eligible = premature_after_threshold

    # 4. 난임시술비에서 remaining threshold 차감
    infertility_after_threshold = max(0, infertility_medical - remaining_threshold)

    infertility_eligible = infertility_after_threshold

    # 세액공제 계산
    general_credit = int((other_eligible + self_eligible) * MEDICAL_RATE_GENERAL)
    premature_credit = int(premature_eligible * MEDICAL_RATE_PREMATURE)
    infertility_credit = int(infertility_eligible * MEDICAL_RATE_INFERTILITY)

    return general_credit + premature_credit + infertility_credit
