"""
주택자금 공제 계산기 테스트 [p.107-119, p.122-123, p.202-204]

TDD: RED phase - 테스트를 먼저 작성합니다.
"""
import pytest

from housing_deduction import (
    calc_housing_loan_deduction,
    calc_rent_tax_credit,
)
from test_data import CASE, HOUSING


# =============================================================================
# calc_housing_loan_deduction (주택자금 소득공제)
# =============================================================================
class TestHousingLoanDeduction:
    """주택자금 소득공제 [p.107-119]."""

    def test_case_kangmo(self):
        """이강모 사례: 장기주택저당차입금 이자 100만원."""
        result = calc_housing_loan_deduction(
            mortgage_interest=HOUSING["mortgage_interest"],
        )
        assert result == HOUSING["deduction"]
        assert result == 1_000_000

    def test_mortgage_only_within_limit(self):
        """장기주택저당차입금만 - 한도 내."""
        result = calc_housing_loan_deduction(
            mortgage_interest=5_000_000,
            mortgage_limit=20_000_000,
        )
        assert result == 5_000_000

    def test_mortgage_exceeds_default_limit(self):
        """장기주택저당차입금 기본한도(2천만원) 초과."""
        result = calc_housing_loan_deduction(
            mortgage_interest=25_000_000,
        )
        assert result == 20_000_000

    def test_mortgage_at_default_limit(self):
        """장기주택저당차입금 정확히 기본한도."""
        result = calc_housing_loan_deduction(
            mortgage_interest=20_000_000,
        )
        assert result == 20_000_000

    def test_mortgage_custom_limit_1800(self):
        """장기주택저당차입금 한도 1800만원 (고정 또는 비거치 15년이상)."""
        result = calc_housing_loan_deduction(
            mortgage_interest=20_000_000,
            mortgage_limit=18_000_000,
        )
        assert result == 18_000_000

    def test_mortgage_custom_limit_800(self):
        """장기주택저당차입금 한도 800만원 (기타 15년이상)."""
        result = calc_housing_loan_deduction(
            mortgage_interest=10_000_000,
            mortgage_limit=8_000_000,
        )
        assert result == 8_000_000

    def test_mortgage_custom_limit_600(self):
        """장기주택저당차입금 한도 600만원 (고정 또는 비거치 10~15년)."""
        result = calc_housing_loan_deduction(
            mortgage_interest=10_000_000,
            mortgage_limit=6_000_000,
        )
        assert result == 6_000_000

    def test_rent_loan_only(self):
        """주택임차차입금만 - 40% 적용."""
        result = calc_housing_loan_deduction(
            rent_loan_repayment=5_000_000,
        )
        # 5,000,000 x 40% = 2,000,000 (400만원 한도 이내)
        assert result == 2_000_000

    def test_rent_loan_exceeds_combined_limit(self):
        """주택임차차입금 - 합산 400만원 한도 초과."""
        result = calc_housing_loan_deduction(
            rent_loan_repayment=15_000_000,
        )
        # 15,000,000 x 40% = 6,000,000 -> 400만원 한도
        assert result == 4_000_000

    def test_rent_loan_at_combined_limit(self):
        """주택임차차입금 - 정확히 합산 한도 도달."""
        result = calc_housing_loan_deduction(
            rent_loan_repayment=10_000_000,
        )
        # 10,000,000 x 40% = 4,000,000 = 400만원 한도
        assert result == 4_000_000

    def test_housing_savings_only(self):
        """주택마련저축만 - 40% 적용."""
        result = calc_housing_loan_deduction(
            housing_savings=2_000_000,
        )
        # 2,000,000 x 40% = 800,000 (한도 이내)
        assert result == 800_000

    def test_housing_savings_exceeds_annual_cap(self):
        """주택마련저축 납입액 300만원 한도 초과."""
        result = calc_housing_loan_deduction(
            housing_savings=5_000_000,
        )
        # capped at 3,000,000, then 3,000,000 x 40% = 1,200,000 (400만원 한도 이내)
        assert result == 1_200_000

    def test_housing_savings_at_annual_cap(self):
        """주택마련저축 납입액 정확히 300만원."""
        result = calc_housing_loan_deduction(
            housing_savings=3_000_000,
        )
        # 3,000,000 x 40% = 1,200,000
        assert result == 1_200_000

    def test_rent_loan_and_savings_combined(self):
        """주택임차 + 주택마련저축 합산 한도 적용."""
        result = calc_housing_loan_deduction(
            rent_loan_repayment=8_000_000,
            housing_savings=3_000_000,
        )
        # rent: 8,000,000 x 40% = 3,200,000
        # savings: 3,000,000 x 40% = 1,200,000
        # combined: 4,400,000 -> 400만원 한도
        assert result == 4_000_000

    def test_rent_loan_and_savings_within_limit(self):
        """주택임차 + 주택마련저축 합산 한도 이내."""
        result = calc_housing_loan_deduction(
            rent_loan_repayment=3_000_000,
            housing_savings=1_000_000,
        )
        # rent: 3,000,000 x 40% = 1,200,000
        # savings: 1,000,000 x 40% = 400,000
        # combined: 1,600,000 (한도 이내)
        assert result == 1_600_000

    def test_all_three_types(self):
        """주택임차 + 주택마련저축 + 장기주택저당 모두."""
        result = calc_housing_loan_deduction(
            rent_loan_repayment=5_000_000,
            housing_savings=2_000_000,
            mortgage_interest=10_000_000,
            mortgage_limit=20_000_000,
        )
        # rent: 5,000,000 x 40% = 2,000,000
        # savings: 2,000,000 x 40% = 800,000
        # combined rent+savings: 2,800,000 (한도 이내)
        # mortgage: 10,000,000 (한도 이내)
        assert result == 2_800_000 + 10_000_000

    def test_all_three_types_at_limits(self):
        """모든 유형 한도 초과."""
        result = calc_housing_loan_deduction(
            rent_loan_repayment=15_000_000,
            housing_savings=5_000_000,
            mortgage_interest=25_000_000,
            mortgage_limit=20_000_000,
        )
        # rent: 15,000,000 x 40% = 6,000,000
        # savings: 3,000,000 x 40% = 1,200,000
        # combined: 7,200,000 -> 400만원 한도
        # mortgage: 25,000,000 -> 2,000만원 한도
        assert result == 4_000_000 + 20_000_000

    def test_zero_all(self):
        """모든 금액이 0인 경우."""
        result = calc_housing_loan_deduction()
        assert result == 0

    def test_boundary_one_won_rent_loan(self):
        """1원 주택임차 경계값."""
        result = calc_housing_loan_deduction(rent_loan_repayment=1)
        # 1 x 40% = 0.4 -> int(0) = 0
        assert result == 0

    def test_boundary_one_won_savings(self):
        """1원 주택마련저축 경계값."""
        result = calc_housing_loan_deduction(housing_savings=1)
        # 1 x 40% = 0.4 -> int(0) = 0
        assert result == 0

    def test_mortgage_zero(self):
        """장기주택저당 0원."""
        result = calc_housing_loan_deduction(mortgage_interest=0)
        assert result == 0


# =============================================================================
# calc_rent_tax_credit (월세액 세액공제)
# =============================================================================
class TestRentTaxCredit:
    """월세액 세액공제 [p.202-204]."""

    def test_salary_under_55m_rate_17(self):
        """총급여 5500만원 이하: 17%."""
        result = calc_rent_tax_credit(
            total_salary=50_000_000,
            annual_rent=6_000_000,
        )
        assert result == int(6_000_000 * 0.17)

    def test_salary_over_55m_rate_15(self):
        """총급여 5500만원 초과 8000만원 이하: 15%."""
        result = calc_rent_tax_credit(
            total_salary=65_000_000,
            annual_rent=6_000_000,
        )
        assert result == int(6_000_000 * 0.15)

    def test_salary_exactly_55m(self):
        """총급여 정확히 5500만원 경계값: 17%."""
        result = calc_rent_tax_credit(
            total_salary=55_000_000,
            annual_rent=6_000_000,
        )
        assert result == int(6_000_000 * 0.17)

    def test_salary_exactly_80m(self):
        """총급여 정확히 8000만원 경계값: 15%."""
        result = calc_rent_tax_credit(
            total_salary=80_000_000,
            annual_rent=6_000_000,
        )
        assert result == int(6_000_000 * 0.15)

    def test_salary_over_80m_ineligible(self):
        """총급여 8000만원 초과: 공제 불가."""
        result = calc_rent_tax_credit(
            total_salary=80_000_001,
            annual_rent=6_000_000,
        )
        assert result == 0

    def test_salary_over_80m_large(self):
        """총급여 1억원: 공제 불가."""
        result = calc_rent_tax_credit(
            total_salary=100_000_000,
            annual_rent=12_000_000,
        )
        assert result == 0

    def test_annual_rent_exceeds_limit(self):
        """연간 월세 1000만원 한도 초과."""
        result = calc_rent_tax_credit(
            total_salary=50_000_000,
            annual_rent=15_000_000,
        )
        # capped at 10,000,000
        assert result == int(10_000_000 * 0.17)

    def test_annual_rent_at_limit(self):
        """연간 월세 정확히 1000만원."""
        result = calc_rent_tax_credit(
            total_salary=50_000_000,
            annual_rent=10_000_000,
        )
        assert result == int(10_000_000 * 0.17)

    def test_zero_rent(self):
        """월세 0원."""
        result = calc_rent_tax_credit(
            total_salary=50_000_000,
            annual_rent=0,
        )
        assert result == 0

    def test_zero_salary(self):
        """총급여 0원 (5500만원 이하이므로 17%)."""
        result = calc_rent_tax_credit(
            total_salary=0,
            annual_rent=5_000_000,
        )
        assert result == int(5_000_000 * 0.17)

    def test_boundary_one_won_rent(self):
        """월세 1원 경계값."""
        result = calc_rent_tax_credit(
            total_salary=50_000_000,
            annual_rent=1,
        )
        # 1 x 0.17 = 0.17 -> 0
        assert result == 0

    def test_low_salary_high_rent(self):
        """저소득 고월세."""
        result = calc_rent_tax_credit(
            total_salary=30_000_000,
            annual_rent=12_000_000,
        )
        # rent capped at 10,000,000
        assert result == int(10_000_000 * 0.17)

    def test_typical_monthly_rent(self):
        """일반적인 월세 60만원 x 12개월."""
        result = calc_rent_tax_credit(
            total_salary=40_000_000,
            annual_rent=7_200_000,
        )
        assert result == int(7_200_000 * 0.17)
