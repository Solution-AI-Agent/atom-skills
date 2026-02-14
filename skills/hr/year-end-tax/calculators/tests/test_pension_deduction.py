"""
연금 공제 계산기 테스트 [p.103-104, p.164-168]

TDD: RED phase - 테스트를 먼저 작성합니다.
"""
import pytest

from pension_deduction import (
    calc_pension_insurance_deduction,
    calc_pension_tax_credit,
)
from test_data import CASE, PENSION


# =============================================================================
# calc_pension_insurance_deduction (연금보험료 소득공제)
# =============================================================================
class TestPensionInsuranceDeduction:
    """연금보험료 소득공제 - 국민연금 전액 공제."""

    def test_case_kangmo(self):
        """이강모 사례: 국민연금 250만원 전액 공제."""
        result = calc_pension_insurance_deduction(
            national_pension=PENSION["national_pension"],
        )
        assert result == CASE["pension_insurance_deduction"]
        assert result == 2_500_000

    def test_zero(self):
        """국민연금 0원."""
        result = calc_pension_insurance_deduction(national_pension=0)
        assert result == 0

    def test_large_amount(self):
        """대금액 - 한도 없음."""
        result = calc_pension_insurance_deduction(national_pension=10_000_000)
        assert result == 10_000_000

    def test_small_amount(self):
        """소액."""
        result = calc_pension_insurance_deduction(national_pension=1)
        assert result == 1


# =============================================================================
# calc_pension_tax_credit (연금계좌 세액공제)
# =============================================================================
class TestPensionTaxCredit:
    """연금계좌 세액공제 (연금저축 + 퇴직연금)."""

    def test_case_kangmo(self):
        """이강모 사례: 연금저축 200만 + 퇴직연금 100만 = 300만 x 12% = 36만."""
        result = calc_pension_tax_credit(
            total_salary=CASE["total_salary"],
            pension_savings=PENSION["pension_savings"],
            retirement_pension=PENSION["retirement_pension"],
        )
        assert result == PENSION["tax_credit"]
        assert result == 360_000

    def test_savings_limit_600man(self):
        """연금저축 한도 600만원."""
        result = calc_pension_tax_credit(
            total_salary=65_400_000,  # > 5,500만 -> 12%
            pension_savings=10_000_000,
            retirement_pension=0,
        )
        # savings: min(10,000,000, 6,000,000) = 6,000,000
        # total: 6,000,000 x 12% = 720,000
        assert result == 720_000

    def test_total_limit_900man(self):
        """합산한도 900만원."""
        result = calc_pension_tax_credit(
            total_salary=65_400_000,  # > 5,500만 -> 12%
            pension_savings=6_000_000,
            retirement_pension=5_000_000,
        )
        # savings: min(6,000,000, 6,000,000) = 6,000,000
        # retirement: min(5,000,000, 9,000,000 - 6,000,000) = 3,000,000
        # total: 9,000,000 x 12% = 1,080,000
        assert result == 1_080_000

    def test_rate_low_salary(self):
        """총급여 5,500만원 이하 -> 15%."""
        result = calc_pension_tax_credit(
            total_salary=55_000_000,
            pension_savings=2_000_000,
            retirement_pension=0,
        )
        # 2,000,000 x 15% = 300,000
        assert result == 300_000

    def test_rate_high_salary(self):
        """총급여 5,500만원 초과 -> 12%."""
        result = calc_pension_tax_credit(
            total_salary=55_000_001,
            pension_savings=2_000_000,
            retirement_pension=0,
        )
        # 2,000,000 x 12% = 240,000
        assert result == 240_000

    def test_rate_boundary_exactly_5500(self):
        """총급여 정확히 5,500만원 -> 15% (이하)."""
        result = calc_pension_tax_credit(
            total_salary=55_000_000,
            pension_savings=1_000_000,
            retirement_pension=0,
        )
        assert result == 150_000  # 1,000,000 x 15%

    def test_zero_savings_and_retirement(self):
        """연금저축 + 퇴직연금 모두 0원."""
        result = calc_pension_tax_credit(
            total_salary=50_000_000,
            pension_savings=0,
            retirement_pension=0,
        )
        assert result == 0

    def test_only_retirement_pension(self):
        """퇴직연금만 있는 경우."""
        result = calc_pension_tax_credit(
            total_salary=50_000_000,  # <= 5,500만 -> 15%
            pension_savings=0,
            retirement_pension=5_000_000,
        )
        # savings: 0 -> savings_eligible = 0
        # retirement: min(5,000,000, 9,000,000 - 0) = 5,000,000
        # total: 5,000,000 x 15% = 750,000
        assert result == 750_000

    def test_retirement_limited_by_combined(self):
        """퇴직연금이 합산한도에 의해 제한."""
        result = calc_pension_tax_credit(
            total_salary=50_000_000,  # <= 5,500만 -> 15%
            pension_savings=5_000_000,
            retirement_pension=10_000_000,
        )
        # savings: min(5,000,000, 6,000,000) = 5,000,000
        # retirement: min(10,000,000, 9,000,000 - 5,000,000) = 4,000,000
        # total: 9,000,000 x 15% = 1,350,000
        assert result == 1_350_000

    def test_retirement_default_zero(self):
        """퇴직연금 기본값 0."""
        result = calc_pension_tax_credit(
            total_salary=50_000_000,
            pension_savings=3_000_000,
        )
        # 3,000,000 x 15% = 450,000
        assert result == 450_000

    def test_savings_at_exact_limit(self):
        """연금저축 정확히 600만원."""
        result = calc_pension_tax_credit(
            total_salary=40_000_000,  # <= 5,500만 -> 15%
            pension_savings=6_000_000,
            retirement_pension=0,
        )
        # savings: 6,000,000
        # total: 6,000,000 x 15% = 900,000
        assert result == 900_000

    def test_max_combined_at_exact_limit(self):
        """합산 정확히 900만원."""
        result = calc_pension_tax_credit(
            total_salary=40_000_000,  # <= 5,500만 -> 15%
            pension_savings=6_000_000,
            retirement_pension=3_000_000,
        )
        # savings: 6,000,000, retirement: 3,000,000
        # total: 9,000,000 x 15% = 1,350,000
        assert result == 1_350_000

    def test_small_salary_high_savings(self):
        """저소득 고저축."""
        result = calc_pension_tax_credit(
            total_salary=30_000_000,  # <= 5,500만 -> 15%
            pension_savings=6_000_000,
            retirement_pension=3_000_000,
        )
        # 9,000,000 x 15% = 1,350,000
        assert result == 1_350_000
