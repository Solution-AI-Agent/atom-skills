"""
기부금 세액공제 계산기 테스트 [p.186-198]

TDD: RED phase - 테스트를 먼저 작성합니다.
"""
import pytest

from donation_deduction import (
    calc_donation_tax_credit,
)
from test_data import CASE, DONATION


# =============================================================================
# calc_donation_tax_credit (기부금 세액공제)
# =============================================================================
class TestDonationTaxCredit:
    """기부금 세액공제 [p.186-198]."""

    def test_case_kangmo(self):
        """이강모 사례: 정치자금 20만 + 고향사랑 10만 + 특례 50만 = 271,818."""
        result = calc_donation_tax_credit(
            earned_income_amount=CASE["earned_income_amount"],
            political=DONATION["political"],
            hometown=DONATION["hometown"],
            special=DONATION["special"],
        )
        assert result == DONATION["total_credit"]
        assert result == 271_818

    def test_political_under_100k(self):
        """정치자금 10만원 이하: 100/110."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            political=100_000,
        )
        # 100,000 x 100/110 = 90,909.0909... -> 90,909
        assert result == 90_909

    def test_political_over_100k_under_30m(self):
        """정치자금 10만원 초과 3천만원 이하: 100/110 + 15%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            political=1_000_000,
        )
        # 100,000 x 100/110 = 90,909
        # 900,000 x 15% = 135,000
        assert result == 90_909 + 135_000

    def test_political_over_30m(self):
        """정치자금 3천만원 초과: 100/110 + 15% + 25%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            political=40_000_000,
        )
        # 100,000 x 100/110 = 90,909
        # 29,900,000 x 15% = 4,485,000
        # 10,000,000 x 25% = 2,500,000
        assert result == 90_909 + 4_485_000 + 2_500_000

    def test_political_exactly_100k(self):
        """정치자금 정확히 10만원 경계값."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            political=100_000,
        )
        assert result == 90_909

    def test_political_exactly_30m(self):
        """정치자금 정확히 3천만원 경계값."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            political=30_000_000,
        )
        # 100,000 x 100/110 = 90,909
        # 29,900,000 x 15% = 4,485,000
        assert result == 90_909 + 4_485_000

    def test_hometown_under_100k(self):
        """고향사랑 10만원 이하: 100/110."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            hometown=50_000,
        )
        # 50,000 x 100/110 = 45,454.5... -> 45,454
        assert result == 45_454

    def test_hometown_exactly_100k(self):
        """고향사랑 정확히 10만원."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            hometown=100_000,
        )
        assert result == 90_909

    def test_hometown_over_100k(self):
        """고향사랑 10만원 초과: 100/110 + 15%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            hometown=500_000,
        )
        # 100,000 x 100/110 = 90,909
        # 400,000 x 15% = 60,000
        assert result == 90_909 + 60_000

    def test_special_under_10m(self):
        """특례기부금 1천만원 이하: 15%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            special=5_000_000,
        )
        assert result == int(5_000_000 * 0.15)

    def test_special_over_10m(self):
        """특례기부금 1천만원 초과: 15% + 30%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            special=15_000_000,
        )
        # 10,000,000 x 15% = 1,500,000
        # 5,000,000 x 30% = 1,500,000
        assert result == 1_500_000 + 1_500_000

    def test_special_exactly_10m(self):
        """특례기부금 정확히 1천만원 경계값."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            special=10_000_000,
        )
        assert result == int(10_000_000 * 0.15)

    def test_esop_under_10m(self):
        """우리사주조합기부금 1천만원 이하: 15%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            esop=3_000_000,
        )
        assert result == int(3_000_000 * 0.15)

    def test_esop_over_10m(self):
        """우리사주조합기부금 1천만원 초과: 15% + 30%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            esop=12_000_000,
        )
        # 10,000,000 x 15% = 1,500,000
        # 2,000,000 x 30% = 600,000
        assert result == 1_500_000 + 600_000

    def test_general_non_religious_under_10m(self):
        """일반기부금(종교외) 1천만원 이하: 15%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            general_non_religious=5_000_000,
        )
        assert result == int(5_000_000 * 0.15)

    def test_general_non_religious_over_10m(self):
        """일반기부금(종교외) 1천만원 초과: 15% + 30%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            general_non_religious=15_000_000,
        )
        # min(15,000,000, limit) then apply rates
        # limit = 50,000,000 x 30% = 15,000,000 (no religious, so 30%)
        # 10,000,000 x 15% + 5,000,000 x 30% = 1,500,000 + 1,500,000
        assert result == 3_000_000

    def test_general_religious_under_10m(self):
        """일반기부금(종교) 1천만원 이하: 15%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            general_religious=3_000_000,
        )
        # limit = 50,000,000 x 10% = 5,000,000 (religious)
        assert result == int(3_000_000 * 0.15)

    def test_general_religious_over_10m(self):
        """일반기부금(종교) 1천만원 초과: 15% + 30%."""
        result = calc_donation_tax_credit(
            earned_income_amount=100_000_000,
            general_religious=15_000_000,
        )
        # limit = 100,000,000 x 10% = 10,000,000
        # capped at 10,000,000
        # 10,000,000 x 15% = 1,500,000
        assert result == 1_500_000

    def test_all_zero(self):
        """모든 기부금 0원."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
        )
        assert result == 0

    def test_zero_earned_income(self):
        """근로소득금액 0원 - 모든 한도 0."""
        result = calc_donation_tax_credit(
            earned_income_amount=0,
            political=100_000,
            hometown=100_000,
            special=500_000,
        )
        assert result == 0

    def test_political_limit_by_earned_income(self):
        """정치자금 한도: 근로소득금액의 100%."""
        result = calc_donation_tax_credit(
            earned_income_amount=100_000,
            political=500_000,
        )
        # political capped at 100,000 (earned_income_amount x 100%)
        # 100,000 x 100/110 = 90,909
        assert result == 90_909

    def test_combined_political_and_hometown(self):
        """정치자금 + 고향사랑 합산."""
        result = calc_donation_tax_credit(
            earned_income_amount=52_380_000,
            political=200_000,
            hometown=100_000,
        )
        # political: 100,000 x 100/110 + 100,000 x 15% = 90,909 + 15,000 = 105,909
        # hometown: 100,000 x 100/110 = 90,909
        assert result == 105_909 + 90_909

    def test_combined_all_types(self):
        """모든 기부금 유형 복합."""
        result = calc_donation_tax_credit(
            earned_income_amount=100_000_000,
            political=200_000,
            hometown=100_000,
            special=5_000_000,
            esop=2_000_000,
            general_non_religious=3_000_000,
            general_religious=1_000_000,
        )
        # political: 90,909 + 15,000 = 105,909
        # hometown: 90,909
        # special: 5,000,000 x 15% = 750,000
        # esop: 2,000,000 x 15% = 300,000
        # general_non_religious: 3,000,000 x 15% = 450,000
        # general_religious: 1,000,000 x 15% = 150,000
        expected = 105_909 + 90_909 + 750_000 + 300_000 + 450_000 + 150_000
        assert result == expected

    def test_esop_limit_30_percent(self):
        """우리사주 한도: 잔여 근로소득금액의 30%."""
        result = calc_donation_tax_credit(
            earned_income_amount=10_000_000,
            esop=10_000_000,
        )
        # esop limit = 10,000,000 x 30% = 3,000,000
        # 3,000,000 x 15% = 450,000
        assert result == 450_000

    def test_general_non_religious_limit_with_religious(self):
        """종교단체 기부금 있을 때 종교외 한도: 잔여의 20%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            general_non_religious=20_000_000,
            general_religious=1_000_000,
        )
        # non_religious limit = 50,000,000 x 20% = 10,000,000 (religious exists)
        # non_religious capped: 10,000,000
        # 10,000,000 x 15% = 1,500,000
        # religious limit = 50,000,000 x 10% = 5,000,000
        # religious: 1,000,000 (within limit)
        # 1,000,000 x 15% = 150,000
        assert result == 1_500_000 + 150_000

    def test_general_non_religious_limit_without_religious(self):
        """종교단체 기부금 없을 때 종교외 한도: 잔여의 30%."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            general_non_religious=20_000_000,
        )
        # non_religious limit = 50,000,000 x 30% = 15,000,000 (no religious)
        # non_religious capped: 15,000,000
        # 10,000,000 x 15% + 5,000,000 x 30% = 1,500,000 + 1,500,000
        assert result == 3_000_000

    def test_boundary_one_won(self):
        """1원 경계값."""
        result = calc_donation_tax_credit(
            earned_income_amount=50_000_000,
            special=1,
        )
        # 1 x 15% = 0.15 -> 0
        assert result == 0

    def test_political_200k_breakdown(self):
        """정치자금 20만원 - 이강모 사례 상세 검증."""
        result = calc_donation_tax_credit(
            earned_income_amount=52_380_000,
            political=200_000,
        )
        # 100,000 x 100/110 = 90,909
        # 100,000 x 15% = 15,000
        assert result == 105_909

    def test_hometown_100k_breakdown(self):
        """고향사랑 10만원 - 이강모 사례 상세 검증."""
        result = calc_donation_tax_credit(
            earned_income_amount=52_380_000,
            hometown=100_000,
        )
        # 100,000 x 100/110 = 90,909
        assert result == 90_909

    def test_special_500k_breakdown(self):
        """특례 50만원 - 이강모 사례 상세 검증."""
        result = calc_donation_tax_credit(
            earned_income_amount=52_380_000,
            special=500_000,
        )
        # 500,000 x 15% = 75,000
        assert result == 75_000

    def test_small_earned_income_cascading_limits(self):
        """소규모 근로소득금액에서 한도 연쇄 효과."""
        result = calc_donation_tax_credit(
            earned_income_amount=1_000_000,
            political=500_000,
            hometown=500_000,
            special=500_000,
        )
        # political limit: 1,000,000, capped at 500,000
        # political credit: 100,000 x 100/110 + 400,000 x 15% = 90,909 + 60,000 = 150,909
        # remaining: 1,000,000 - 500,000 = 500,000
        # hometown limit: 500,000, capped at 500,000
        # hometown credit: 100,000 x 100/110 + 400,000 x 15% = 90,909 + 60,000 = 150,909
        # remaining: 500,000 - 500,000 = 0
        # special limit: 0, capped at 0
        # special credit: 0
        assert result == 150_909 + 150_909
