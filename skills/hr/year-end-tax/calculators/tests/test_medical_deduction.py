"""
의료비 세액공제 계산기 테스트 [p.172-177]

TDD: RED phase - 테스트를 먼저 작성합니다.
"""
import pytest

from medical_deduction import (
    calc_medical_tax_credit,
)
from test_data import CASE, MEDICAL


# =============================================================================
# calc_medical_tax_credit (의료비 세액공제)
# =============================================================================
class TestMedicalTaxCredit:
    """의료비 세액공제 계산."""

    def test_case_kangmo(self):
        """이강모 사례: 의료비 세액공제 950,700원."""
        result = calc_medical_tax_credit(
            total_salary=CASE["total_salary"],
            other_dependent_medical=4_500_000,  # 배우자수술 250만 + 산후조리원한도 200만
            self_etc_medical=1_800_000,         # 입원 130만 + 안경한도 50만
            infertility_medical=MEDICAL["spouse_infertility"],
        )
        assert result == MEDICAL["tax_credit"]
        assert result == 950_700

    def test_threshold_calculation(self):
        """총급여액 3% 기준금액 검증."""
        # 65,400,000 x 3% = 1,962,000
        result = calc_medical_tax_credit(
            total_salary=65_400_000,
            other_dependent_medical=1_962_000,
            self_etc_medical=0,
        )
        # other_dependent: 1,962,000 - 1,962,000 = 0
        assert result == 0

    def test_threshold_subtracted_from_other_dependent_first(self):
        """기준금액이 그 외 부양가족에서 먼저 차감됨."""
        result = calc_medical_tax_credit(
            total_salary=10_000_000,  # threshold = 300,000
            other_dependent_medical=500_000,
            self_etc_medical=200_000,
        )
        # other_dependent: 500,000 - 300,000 = 200,000
        # self_etc: 200,000 (no further threshold)
        # credit: (200,000 + 200,000) x 15% = 60,000
        assert result == 60_000

    def test_threshold_overflows_to_self_etc(self):
        """기준금액이 그 외 부양가족을 초과하면 본인등으로 이월."""
        result = calc_medical_tax_credit(
            total_salary=100_000_000,  # threshold = 3,000,000
            other_dependent_medical=1_000_000,
            self_etc_medical=5_000_000,
        )
        # other_dependent: 1,000,000 - 3,000,000 -> 0, remaining threshold = 2,000,000
        # self_etc: 5,000,000 - 2,000,000 = 3,000,000
        # credit: (0 + 3,000,000) x 15% = 450,000
        assert result == 450_000

    def test_threshold_overflows_to_premature(self):
        """기준금액이 본인등도 초과하면 미숙아로 이월."""
        result = calc_medical_tax_credit(
            total_salary=100_000_000,  # threshold = 3,000,000
            other_dependent_medical=0,
            self_etc_medical=1_000_000,
            premature_medical=5_000_000,
        )
        # other_dependent: 0 - 3,000,000 -> 0, remaining = 3,000,000
        # self_etc: 1,000,000 - 3,000,000 -> 0, remaining = 2,000,000
        # premature: 5,000,000 - 2,000,000 = 3,000,000
        # credit: 3,000,000 x 20% = 600,000
        assert result == 600_000

    def test_threshold_overflows_to_infertility(self):
        """기준금액이 미숙아도 초과하면 난임시술비로 이월."""
        result = calc_medical_tax_credit(
            total_salary=100_000_000,  # threshold = 3,000,000
            other_dependent_medical=0,
            self_etc_medical=0,
            premature_medical=1_000_000,
            infertility_medical=5_000_000,
        )
        # other_dependent: 0, remaining = 3,000,000
        # self_etc: 0, remaining = 3,000,000
        # premature: 1,000,000 - 3,000,000 -> 0, remaining = 2,000,000
        # infertility: 5,000,000 - 2,000,000 = 3,000,000
        # credit: 3,000,000 x 30% = 900,000
        assert result == 900_000

    def test_other_dependent_limit_700man(self):
        """그 외 부양가족 700만원 한도."""
        result = calc_medical_tax_credit(
            total_salary=10_000_000,  # threshold = 300,000
            other_dependent_medical=10_000_000,
            self_etc_medical=0,
        )
        # other_dependent: 10,000,000 - 300,000 = 9,700,000 -> min(9,700,000, 7,000,000) = 7,000,000
        # credit: 7,000,000 x 15% = 1,050,000
        assert result == 1_050_000

    def test_self_etc_no_limit(self):
        """본인등 의료비 한도 없음."""
        result = calc_medical_tax_credit(
            total_salary=10_000_000,  # threshold = 300,000
            other_dependent_medical=300_000,  # exactly covers threshold
            self_etc_medical=50_000_000,
        )
        # other_dependent: 300,000 - 300,000 = 0
        # self_etc: 50,000,000 (no limit)
        # credit: 50,000,000 x 15% = 7,500,000
        assert result == 7_500_000

    def test_infertility_rate_30_percent(self):
        """난임시술비 30% 적용."""
        result = calc_medical_tax_credit(
            total_salary=10_000_000,  # threshold = 300,000
            other_dependent_medical=300_000,  # covers threshold
            self_etc_medical=0,
            infertility_medical=2_000_000,
        )
        # infertility: 2,000,000 x 30% = 600,000
        assert result == 600_000

    def test_premature_rate_20_percent(self):
        """미숙아/선천성이상아 20% 적용."""
        result = calc_medical_tax_credit(
            total_salary=10_000_000,  # threshold = 300,000
            other_dependent_medical=300_000,  # covers threshold
            self_etc_medical=0,
            premature_medical=3_000_000,
        )
        # premature: 3,000,000 x 20% = 600,000
        assert result == 600_000

    def test_all_categories(self):
        """모든 카테고리 동시 적용."""
        result = calc_medical_tax_credit(
            total_salary=10_000_000,  # threshold = 300,000
            other_dependent_medical=1_300_000,
            self_etc_medical=500_000,
            infertility_medical=1_000_000,
            premature_medical=800_000,
        )
        # other_dependent: 1,300,000 - 300,000 = 1,000,000 (under 700만 limit)
        # self_etc: 500,000
        # premature: 800,000
        # infertility: 1,000,000
        # credit: (1,000,000 + 500,000) x 15% + 800,000 x 20% + 1,000,000 x 30%
        #       = 225,000 + 160,000 + 300,000 = 685,000
        assert result == 685_000

    def test_all_zero(self):
        """모든 금액이 0인 경우."""
        result = calc_medical_tax_credit(
            total_salary=50_000_000,
            other_dependent_medical=0,
            self_etc_medical=0,
        )
        assert result == 0

    def test_below_threshold(self):
        """총 의료비가 기준금액 미만."""
        result = calc_medical_tax_credit(
            total_salary=50_000_000,  # threshold = 1,500,000
            other_dependent_medical=1_000_000,
            self_etc_medical=0,
        )
        # other_dependent: 1,000,000 - 1,500,000 -> 0
        assert result == 0

    def test_zero_salary(self):
        """총급여액 0원 (threshold = 0)."""
        result = calc_medical_tax_credit(
            total_salary=0,
            other_dependent_medical=500_000,
            self_etc_medical=300_000,
        )
        # threshold = 0
        # other_dependent: 500,000
        # self_etc: 300,000
        # credit: (500,000 + 300,000) x 15% = 120,000
        assert result == 120_000

    def test_only_infertility_with_threshold(self):
        """난임시술비만 있고 기준금액 차감."""
        result = calc_medical_tax_credit(
            total_salary=20_000_000,  # threshold = 600,000
            other_dependent_medical=0,
            self_etc_medical=0,
            infertility_medical=2_000_000,
        )
        # other_dependent: 0, remaining = 600,000
        # self_etc: 0, remaining = 600,000
        # premature: 0, remaining = 600,000
        # infertility: 2,000,000 - 600,000 = 1,400,000
        # credit: 1,400,000 x 30% = 420,000
        assert result == 420_000

    def test_defaults_for_optional_params(self):
        """선택 파라미터 기본값 0."""
        result = calc_medical_tax_credit(
            total_salary=10_000_000,
            other_dependent_medical=1_000_000,
            self_etc_medical=0,
        )
        # threshold = 300,000
        # other_dependent: 1,000,000 - 300,000 = 700,000
        # credit: 700,000 x 15% = 105,000
        assert result == 105_000
