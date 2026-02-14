"""
Tests for income_tax.py - 근로소득공제, 산출세액, 근로소득세액공제

TDD RED phase: Write tests first, then implement.
All amounts in KRW (원).
"""

from income_tax import (
    calc_earned_income_deduction,
    calc_earned_income_amount,
    calc_taxable_income,
    calc_calculated_tax,
    calc_earned_income_tax_credit,
)
from test_data import CASE


# =============================================================================
# calc_earned_income_deduction (근로소득공제) [p.94]
# =============================================================================
class TestCalcEarnedIncomeDeduction:
    """근로소득공제 계산 테스트"""

    def test_zero_salary(self):
        """총급여액 0원이면 공제도 0원"""
        assert calc_earned_income_deduction(0) == 0

    def test_lowest_bracket(self):
        """500만원 이하 구간: 총급여 x 70%"""
        # 5_000_000 * 0.70 = 3_500_000
        assert calc_earned_income_deduction(5_000_000) == 3_500_000

    def test_lowest_bracket_partial(self):
        """500만원 이하 구간 중간값"""
        # 3_000_000 * 0.70 = 2_100_000
        assert calc_earned_income_deduction(3_000_000) == 2_100_000

    def test_second_bracket(self):
        """500만~1,500만원 구간: 350만원 + (총급여-500만원) x 40%"""
        # 3_500_000 + (10_000_000 - 5_000_000) * 0.40 = 3_500_000 + 2_000_000 = 5_500_000
        assert calc_earned_income_deduction(10_000_000) == 5_500_000

    def test_second_bracket_upper(self):
        """500만~1,500만원 구간 상한"""
        # 3_500_000 + (15_000_000 - 5_000_000) * 0.40 = 3_500_000 + 4_000_000 = 7_500_000
        assert calc_earned_income_deduction(15_000_000) == 7_500_000

    def test_third_bracket(self):
        """1,500만~4,500만원 구간: 750만원 + (총급여-1,500만원) x 15%"""
        # 7_500_000 + (30_000_000 - 15_000_000) * 0.15 = 7_500_000 + 2_250_000 = 9_750_000
        assert calc_earned_income_deduction(30_000_000) == 9_750_000

    def test_fourth_bracket_case_kangmo(self):
        """이강모 사례: 총급여 65,400,000"""
        # 12_000_000 + (65_400_000 - 45_000_000) * 0.05 = 12_000_000 + 1_020_000 = 13_020_000
        assert calc_earned_income_deduction(65_400_000) == 13_020_000

    def test_fourth_bracket_upper(self):
        """4,500만~1억원 구간 상한"""
        # 12_000_000 + (100_000_000 - 45_000_000) * 0.05 = 12_000_000 + 2_750_000 = 14_750_000
        assert calc_earned_income_deduction(100_000_000) == 14_750_000

    def test_highest_bracket(self):
        """1억원 초과 구간: 1,475만원 + (총급여-1억원) x 2%"""
        # 14_750_000 + (100_000_001 - 100_000_000) * 0.02 = 14_750_000 + 0.02 -> 14_750_000 (int)
        assert calc_earned_income_deduction(100_000_001) == 14_750_000

    def test_highest_bracket_large(self):
        """1억원 초과 구간 큰 금액"""
        # 14_750_000 + (200_000_000 - 100_000_000) * 0.02 = 14_750_000 + 2_000_000 = 16_750_000
        assert calc_earned_income_deduction(200_000_000) == 16_750_000

    def test_deduction_cap(self):
        """공제한도 2,000만원 초과 불가"""
        # Very large salary: 14_750_000 + (500_000_000 - 100_000_000) * 0.02
        # = 14_750_000 + 8_000_000 = 22_750_000 -> capped at 20_000_000
        assert calc_earned_income_deduction(500_000_000) == 20_000_000

    def test_matches_test_data(self):
        """이강모 테스트 데이터 검증"""
        assert calc_earned_income_deduction(CASE["total_salary"]) == CASE["earned_income_deduction"]


# =============================================================================
# calc_earned_income_amount (근로소득금액)
# =============================================================================
class TestCalcEarnedIncomeAmount:
    """근로소득금액 = 총급여액 - 근로소득공제"""

    def test_basic(self):
        """기본 계산"""
        assert calc_earned_income_amount(65_400_000) == 52_380_000

    def test_zero_salary(self):
        """총급여액 0원"""
        assert calc_earned_income_amount(0) == 0

    def test_matches_test_data(self):
        """이강모 테스트 데이터 검증"""
        assert calc_earned_income_amount(CASE["total_salary"]) == CASE["earned_income_amount"]


# =============================================================================
# calc_taxable_income (과세표준)
# =============================================================================
class TestCalcTaxableIncome:
    """과세표준 = 근로소득금액 - 소득공제합계"""

    def test_basic(self):
        """기본 계산"""
        assert calc_taxable_income(52_380_000, 16_095_000) == 36_285_000

    def test_cannot_be_negative(self):
        """과세표준은 음수가 될 수 없음"""
        assert calc_taxable_income(1_000_000, 5_000_000) == 0

    def test_zero_deductions(self):
        """공제 없는 경우"""
        assert calc_taxable_income(50_000_000, 0) == 50_000_000

    def test_exact_match(self):
        """소득금액과 공제가 동일한 경우"""
        assert calc_taxable_income(10_000_000, 10_000_000) == 0

    def test_matches_test_data(self):
        """이강모 테스트 데이터 검증"""
        earned_income_amount = CASE["earned_income_amount"]
        total_deductions = CASE["total_income_deduction"] + CASE["card_deduction"]
        assert calc_taxable_income(earned_income_amount, total_deductions) == CASE["taxable_income"]


# =============================================================================
# calc_calculated_tax (산출세액) [p.83]
# =============================================================================
class TestCalcCalculatedTax:
    """산출세액: 과세표준에 기본세율 적용"""

    def test_zero_income(self):
        """과세표준 0원"""
        assert calc_calculated_tax(0) == 0

    def test_bracket_1_boundary(self):
        """1,400만원 이하: 6%"""
        # 14_000_000 * 0.06 - 0 = 840_000
        assert calc_calculated_tax(14_000_000) == 840_000

    def test_bracket_1_mid(self):
        """1,400만원 이하 구간 중간값"""
        # 10_000_000 * 0.06 = 600_000
        assert calc_calculated_tax(10_000_000) == 600_000

    def test_bracket_2_boundary(self):
        """5,000만원 경계: 15% - 126만원"""
        # 50_000_000 * 0.15 - 1_260_000 = 7_500_000 - 1_260_000 = 6_240_000
        assert calc_calculated_tax(50_000_000) == 6_240_000

    def test_bracket_2_just_above_1(self):
        """1,400만원 바로 초과"""
        # 14_000_001 * 0.15 - 1_260_000 = 2_100_000.15 - 1_260_000 = 840_000.15 -> 840_000
        assert calc_calculated_tax(14_000_001) == 840_000

    def test_bracket_3_boundary(self):
        """8,800만원 경계: 24% - 576만원"""
        # 88_000_000 * 0.24 - 5_760_000 = 21_120_000 - 5_760_000 = 15_360_000
        assert calc_calculated_tax(88_000_000) == 15_360_000

    def test_bracket_4_boundary(self):
        """1.5억원 경계: 35% - 1,544만원"""
        # 150_000_000 * 0.35 - 15_440_000 = 52_500_000 - 15_440_000 = 37_060_000
        assert calc_calculated_tax(150_000_000) == 37_060_000

    def test_bracket_5_boundary(self):
        """3억원 경계: 38% - 1,994만원"""
        # 300_000_000 * 0.38 - 19_940_000 = 114_000_000 - 19_940_000 = 94_060_000
        assert calc_calculated_tax(300_000_000) == 94_060_000

    def test_bracket_6_boundary(self):
        """5억원 경계: 40% - 2,594만원"""
        # 500_000_000 * 0.40 - 25_940_000 = 200_000_000 - 25_940_000 = 174_060_000
        assert calc_calculated_tax(500_000_000) == 174_060_000

    def test_bracket_7_boundary(self):
        """10억원 경계: 42% - 3,594만원"""
        # 1_000_000_000 * 0.42 - 35_940_000 = 420_000_000 - 35_940_000 = 384_060_000
        assert calc_calculated_tax(1_000_000_000) == 384_060_000

    def test_bracket_8_over_1b(self):
        """10억원 초과: 45% - 6,594만원"""
        # 1_500_000_000 * 0.45 - 65_940_000 = 675_000_000 - 65_940_000 = 609_060_000
        assert calc_calculated_tax(1_500_000_000) == 609_060_000

    def test_case_kangmo(self):
        """이강모 사례: 과세표준 36,285,000"""
        # 36_285_000 * 0.15 - 1_260_000 = 5_442_750 - 1_260_000 = 4_182_750
        assert calc_calculated_tax(36_285_000) == 4_182_750

    def test_matches_test_data(self):
        """이강모 테스트 데이터 검증"""
        assert calc_calculated_tax(CASE["taxable_income"]) == CASE["calculated_tax"]


# =============================================================================
# calc_earned_income_tax_credit (근로소득세액공제) [p.162-163]
# =============================================================================
class TestCalcEarnedIncomeTaxCredit:
    """근로소득세액공제 테스트"""

    def test_zero_tax(self):
        """산출세액 0원"""
        assert calc_earned_income_tax_credit(0, 65_400_000) == 0

    def test_low_tax_rate(self):
        """산출세액 130만원 이하: 55%"""
        # credit = 1_000_000 * 0.55 = 550_000
        # salary 30M -> limit 740_000, so credit = 550_000
        assert calc_earned_income_tax_credit(1_000_000, 30_000_000) == 550_000

    def test_low_tax_at_threshold(self):
        """산출세액 정확히 130만원"""
        # credit = 1_300_000 * 0.55 = 715_000
        # salary 30M -> limit 740_000, so credit = 715_000
        assert calc_earned_income_tax_credit(1_300_000, 30_000_000) == 715_000

    def test_high_tax_rate(self):
        """산출세액 130만원 초과: 71.5만원 + (산출세액-130만원) x 30%"""
        # credit = 715_000 + (2_000_000 - 1_300_000) * 0.30 = 715_000 + 210_000 = 925_000
        # salary 30M -> limit 740_000, so credit = 740_000
        assert calc_earned_income_tax_credit(2_000_000, 30_000_000) == 740_000

    def test_limit_bracket_under_33m(self):
        """총급여 3,300만원 이하: 한도 74만원"""
        # Large tax so base credit > limit
        # credit = 715_000 + (5_000_000 - 1_300_000) * 0.30 = 715_000 + 1_110_000 = 1_825_000
        # limit = 740_000
        assert calc_earned_income_tax_credit(5_000_000, 33_000_000) == 740_000

    def test_limit_bracket_33m_to_70m_min(self):
        """총급여 3,300만~7,000만원: 한도 = max(74만 - (총급여-3,300만) x 0.008, 66만)"""
        # salary 65.4M: limit = max(740_000 - (65.4M - 33M) * 0.008, 660_000)
        # = max(740_000 - 259_200, 660_000) = max(480_800, 660_000) = 660_000
        # credit = 715_000 + (4_182_750 - 1_300_000) * 0.30 = 715_000 + 864_825 = 1_579_825
        # result = min(1_579_825, 660_000) = 660_000
        assert calc_earned_income_tax_credit(4_182_750, 65_400_000) == 660_000

    def test_limit_bracket_70m_to_120m(self):
        """총급여 7,000만~1.2억원: 한도 = max(66만 - (총급여-7,000만) x 0.5, 50만)"""
        # salary 80M: limit = max(660_000 - (80M - 70M) * 0.5, 500_000)
        # = max(660_000 - 5_000_000, 500_000) = max(-4_340_000, 500_000) = 500_000
        # credit (assume large tax) -> capped at 500_000
        assert calc_earned_income_tax_credit(10_000_000, 80_000_000) == 500_000

    def test_limit_bracket_over_120m(self):
        """총급여 1.2억원 초과: 한도 = max(50만 - (총급여-1.2억) x 0.5, 20만)"""
        # salary 130M: limit = max(500_000 - (130M - 120M) * 0.5, 200_000)
        # = max(500_000 - 5_000_000, 200_000) = max(-4_500_000, 200_000) = 200_000
        assert calc_earned_income_tax_credit(20_000_000, 130_000_000) == 200_000

    def test_credit_less_than_limit(self):
        """세액공제액이 한도보다 작은 경우 세액공제액 그대로"""
        # credit = 500_000 * 0.55 = 275_000
        # salary 30M -> limit 740_000
        # result = 275_000
        assert calc_earned_income_tax_credit(500_000, 30_000_000) == 275_000

    def test_matches_test_data(self):
        """이강모 테스트 데이터 검증"""
        assert calc_earned_income_tax_credit(
            CASE["calculated_tax"], CASE["total_salary"]
        ) == CASE["earned_income_tax_credit"]
