"""
보험료 공제 계산기 테스트 [p.106-107, p.169-172]

TDD: RED phase - 테스트를 먼저 작성합니다.
"""
from insurance_deduction import (
    calc_insurance_income_deduction,
    calc_insurance_tax_credit,
)
from test_data import CASE, INSURANCE


# =============================================================================
# calc_insurance_income_deduction (소득공제: 건강보험료 등)
# =============================================================================
class TestInsuranceIncomeDeduction:
    """국민건강보험료 등 소득공제 - 전액 공제, 한도 없음."""

    def test_case_kangmo(self):
        """이강모 사례: 건강 130만 + 장기요양 40만 = 170만."""
        result = calc_insurance_income_deduction(
            health_insurance=INSURANCE["health_insurance"],
            long_term_care=INSURANCE["long_term_care"],
        )
        assert result == INSURANCE["income_deduction_total"]
        assert result == 1_700_000

    def test_with_employment_insurance(self):
        """고용보험료 포함 시 합산."""
        result = calc_insurance_income_deduction(
            health_insurance=1_000_000,
            long_term_care=200_000,
            employment_insurance=300_000,
        )
        assert result == 1_500_000

    def test_zero_amounts(self):
        """모든 금액이 0인 경우."""
        result = calc_insurance_income_deduction(0, 0, 0)
        assert result == 0

    def test_large_amounts_no_limit(self):
        """대금액 - 한도 없음 확인."""
        result = calc_insurance_income_deduction(
            health_insurance=50_000_000,
            long_term_care=10_000_000,
            employment_insurance=5_000_000,
        )
        assert result == 65_000_000

    def test_employment_insurance_default_zero(self):
        """고용보험 기본값 0."""
        result = calc_insurance_income_deduction(1_000_000, 200_000)
        assert result == 1_200_000


# =============================================================================
# calc_insurance_tax_credit (세액공제: 보장성보험료)
# =============================================================================
class TestInsuranceTaxCredit:
    """보장성보험료 세액공제."""

    def test_case_kangmo_basic(self):
        """이강모 사례: 보장성보험 100만원 한도, 12%."""
        result = calc_insurance_tax_credit(
            protection_premium=INSURANCE["protection_eligible"],
        )
        assert result == INSURANCE["tax_credit"]
        assert result == 120_000

    def test_protection_at_limit(self):
        """보장성보험 정확히 100만원."""
        result = calc_insurance_tax_credit(protection_premium=1_000_000)
        assert result == 120_000

    def test_protection_exceeds_limit(self):
        """보장성보험 300만원 -> 100만원 한도 적용."""
        result = calc_insurance_tax_credit(protection_premium=3_000_000)
        assert result == 120_000

    def test_protection_below_limit(self):
        """보장성보험 50만원 - 한도 내."""
        result = calc_insurance_tax_credit(protection_premium=500_000)
        assert result == 60_000

    def test_zero_protection(self):
        """보장성보험 0원."""
        result = calc_insurance_tax_credit(protection_premium=0)
        assert result == 0

    def test_disabled_only(self):
        """장애인전용보험만 있는 경우: 100만원 한도, 15%."""
        result = calc_insurance_tax_credit(
            protection_premium=0,
            disabled_protection_premium=800_000,
        )
        assert result == 120_000  # 800,000 x 15%

    def test_disabled_exceeds_limit(self):
        """장애인전용 200만원 -> 100만원 한도, 15%."""
        result = calc_insurance_tax_credit(
            protection_premium=0,
            disabled_protection_premium=2_000_000,
        )
        assert result == 150_000  # 1,000,000 x 15%

    def test_both_protection_and_disabled(self):
        """보장성 + 장애인전용 각각 별도 한도."""
        result = calc_insurance_tax_credit(
            protection_premium=1_500_000,
            disabled_protection_premium=1_500_000,
        )
        # 보장성: min(1,500,000, 1,000,000) x 12% = 120,000
        # 장애인: min(1,500,000, 1,000,000) x 15% = 150,000
        assert result == 270_000

    def test_both_below_limits(self):
        """보장성 + 장애인전용 모두 한도 이내."""
        result = calc_insurance_tax_credit(
            protection_premium=500_000,
            disabled_protection_premium=300_000,
        )
        # 500,000 x 12% = 60,000
        # 300,000 x 15% = 45,000
        assert result == 105_000

    def test_disabled_default_zero(self):
        """장애인전용 기본값 0."""
        result = calc_insurance_tax_credit(protection_premium=1_000_000)
        assert result == 120_000

    def test_both_zero(self):
        """보장성 + 장애인전용 모두 0원."""
        result = calc_insurance_tax_credit(
            protection_premium=0,
            disabled_protection_premium=0,
        )
        assert result == 0

    def test_boundary_one_won(self):
        """1원 경계값."""
        result = calc_insurance_tax_credit(protection_premium=1)
        # 1 x 12% = 0.12 -> int(0.12) = 0 (floor)
        assert result == 0
