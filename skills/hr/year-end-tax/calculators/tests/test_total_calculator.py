"""
통합 연말정산 계산기 테스트

TDD: RED phase - 테스트를 먼저 작성합니다.
"""
import pytest

from total_calculator import (
    calc_year_end_tax,
)
from test_data import CASE


# =============================================================================
# 이강모 종합사례 [p.212-219]
# =============================================================================
class TestYearEndTaxKangmoCase:
    """이강모 사례를 통한 통합 연말정산 검증 (가장 중요한 테스트)."""

    @pytest.fixture
    def kangmo_result(self):
        """이강모 사례 결과."""
        return calc_year_end_tax(
            total_salary=65_400_000,
            num_dependents=4,
            national_pension=2_500_000,
            health_insurance=1_300_000,
            long_term_care=400_000,
            housing_loan_deduction=1_000_000,
            card_deduction=4_895_000,
            children_over_8=1,
            birth_orders=[3],
            pension_savings=2_000_000,
            retirement_pension=1_000_000,
            insurance_tax_credit=120_000,
            medical_tax_credit=950_700,
            education_tax_credit=630_000,
            donation_tax_credit=271_818,
            prepaid_tax=1_000_000,
        )

    def test_earned_income_deduction(self, kangmo_result):
        """근로소득공제 = 13,020,000원.

        총급여 65,400,000 -> 4,500만~1억 구간
        = 12,000,000 + (65,400,000 - 45,000,000) x 5%
        = 12,000,000 + 1,020,000 = 13,020,000
        """
        assert kangmo_result["earned_income_deduction"] == CASE["earned_income_deduction"]
        assert kangmo_result["earned_income_deduction"] == 13_020_000

    def test_earned_income_amount(self, kangmo_result):
        """근로소득금액 = 총급여 - 근로소득공제.

        65,400,000 - 13,020,000 = 52,380,000
        """
        assert kangmo_result["earned_income_amount"] == CASE["earned_income_amount"]
        assert kangmo_result["earned_income_amount"] == 52_380_000

    def test_personal_deduction(self, kangmo_result):
        """인적공제 = 4명 x 150만원 = 6,000,000원.

        본인(1) + 자녀3명(이태희6세, 이태현19세, 이태영0세).
        배우자는 소득초과로 제외.
        """
        assert kangmo_result["personal_deduction"] == CASE["personal_deduction"]
        assert kangmo_result["personal_deduction"] == 6_000_000

    def test_pension_insurance_deduction(self, kangmo_result):
        """연금보험료(국민연금) 소득공제 = 2,500,000원."""
        assert kangmo_result["pension_insurance_deduction"] == 2_500_000

    def test_insurance_income_deduction(self, kangmo_result):
        """건강보험 + 장기요양 소득공제 = 1,700,000원.

        건강보험 1,300,000 + 장기요양 400,000 = 1,700,000
        """
        assert kangmo_result["insurance_income_deduction"] == CASE["health_insurance_deduction"]
        assert kangmo_result["insurance_income_deduction"] == 1_700_000

    def test_housing_deduction(self, kangmo_result):
        """주택자금 소득공제 = 1,000,000원."""
        assert kangmo_result["housing_deduction"] == CASE["housing_deduction"]
        assert kangmo_result["housing_deduction"] == 1_000_000

    def test_card_deduction(self, kangmo_result):
        """신용카드등 소득공제 = 4,895,000원."""
        assert kangmo_result["card_deduction"] == CASE["card_deduction"]
        assert kangmo_result["card_deduction"] == 4_895_000

    def test_total_income_deduction(self, kangmo_result):
        """종합소득공제 합계 = 11,200,000원.

        인적(6M) + 연금(2.5M) + 건강보험등(1.7M) + 주택(1M) = 11,200,000
        (신용카드 공제는 별도 적용)
        """
        assert kangmo_result["total_income_deduction"] == CASE["total_income_deduction"]
        assert kangmo_result["total_income_deduction"] == 11_200_000

    def test_taxable_income(self, kangmo_result):
        """과세표준 = 36,285,000원.

        근로소득금액(52,380,000) - 소득공제합계(11,200,000) - 카드공제(4,895,000)
        = 36,285,000
        """
        assert kangmo_result["taxable_income"] == CASE["taxable_income"]
        assert kangmo_result["taxable_income"] == 36_285_000

    def test_calculated_tax(self, kangmo_result):
        """산출세액 = 4,182,750원.

        과세표준 36,285,000 -> 1,400만~5,000만 구간
        = 36,285,000 x 15% - 1,260,000 = 5,442,750 - 1,260,000 = 4,182,750
        """
        assert kangmo_result["calculated_tax"] == CASE["calculated_tax"]
        assert kangmo_result["calculated_tax"] == 4_182_750

    def test_earned_income_tax_credit(self, kangmo_result):
        """근로소득세액공제 = 660,000원.

        산출세액 4,182,750 > 130만원:
        = 715,000 + (4,182,750 - 1,300,000) x 30% = 715,000 + 864,825 = 1,579,825

        한도 (총급여 3,300만~7,000만):
        = max(740,000 - (65,400,000 - 33,000,000) x 0.008, 660,000)
        = max(740,000 - 259,200, 660,000) = max(480,800, 660,000) = 660,000

        공제 = min(1,579,825, 660,000) = 660,000
        """
        assert kangmo_result["earned_income_tax_credit"] == CASE["earned_income_tax_credit"]
        assert kangmo_result["earned_income_tax_credit"] == 660_000

    def test_child_tax_credit(self, kangmo_result):
        """자녀세액공제 = 950,000원.

        8세 이상 1명: 250,000
        출산 셋째: 700,000
        합계: 950,000
        """
        assert kangmo_result["child_tax_credit"] == CASE["child_tax_credit"]
        assert kangmo_result["child_tax_credit"] == 950_000

    def test_pension_tax_credit(self, kangmo_result):
        """연금계좌세액공제 = 360,000원.

        연금저축 200만 + 퇴직연금 100만 = 300만
        공제율 12% (총급여 5,500만원 초과)
        = 3,000,000 x 12% = 360,000
        """
        assert kangmo_result["pension_tax_credit"] == CASE["pension_tax_credit"]
        assert kangmo_result["pension_tax_credit"] == 360_000

    def test_special_tax_credit(self, kangmo_result):
        """특별세액공제 = 보험+의료+교육+기부금 = 1,972,518원."""
        assert kangmo_result["special_tax_credit"] == CASE["special_tax_credit_total"]
        assert kangmo_result["special_tax_credit"] == 1_972_518

    def test_total_tax_credit(self, kangmo_result):
        """세액공제 합계.

        근로소득(660,000) + 자녀(950,000) + 연금(360,000) + 특별(1,972,518)
        = 3,942,518
        """
        assert kangmo_result["total_tax_credit"] == 3_942_518

    def test_determined_tax(self, kangmo_result):
        """결정세액 = 240,232원.

        산출세액(4,182,750) - 세액공제(3,942,518) = 240,232
        """
        assert kangmo_result["determined_tax"] == CASE["determined_tax"]
        assert kangmo_result["determined_tax"] == 240_232

    def test_refund_amount(self, kangmo_result):
        """환급세액 = -759,768원 (음수 = 환급).

        결정세액(240,232) - 기납부세액(1,000,000) = -759,768
        """
        assert kangmo_result["refund_amount"] == CASE["refund_amount"]
        assert kangmo_result["refund_amount"] == -759_768


# =============================================================================
# 반환값 구조 검증
# =============================================================================
class TestReturnStructure:
    """반환 dict 구조 검증."""

    @pytest.fixture
    def result(self):
        """기본 결과."""
        return calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=1,
            prepaid_tax=500_000,
        )

    def test_returns_dict(self, result):
        """반환값은 dict."""
        assert isinstance(result, dict)

    def test_has_all_required_keys(self, result):
        """모든 필수 키 존재."""
        required_keys = [
            "total_salary",
            "earned_income_deduction",
            "earned_income_amount",
            "personal_deduction",
            "pension_insurance_deduction",
            "insurance_income_deduction",
            "housing_deduction",
            "card_deduction",
            "total_income_deduction",
            "taxable_income",
            "calculated_tax",
            "earned_income_tax_credit",
            "child_tax_credit",
            "pension_tax_credit",
            "special_tax_credit",
            "total_tax_credit",
            "determined_tax",
            "prepaid_tax",
            "refund_amount",
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_all_values_are_int(self, result):
        """모든 값은 정수(원)."""
        for key, value in result.items():
            assert isinstance(value, int), f"{key} is not int: {type(value)}"


# =============================================================================
# 소득공제 관련 검증
# =============================================================================
class TestIncomeDeductions:
    """소득공제 계산 검증."""

    def test_personal_deduction_single(self):
        """본인만 있는 경우: 1명 x 150만원."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=1,
        )
        assert result["personal_deduction"] == 1_500_000

    def test_personal_deduction_family(self):
        """가족 있는 경우: 5명 x 150만원."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=5,
        )
        assert result["personal_deduction"] == 7_500_000

    def test_additional_deduction_elderly(self):
        """경로우대 추가공제."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=2,
            elderly_count=1,
        )
        # 기본(3M) + 경로우대(1M) = 4M
        assert result["personal_deduction"] == 4_000_000

    def test_additional_deduction_disabled(self):
        """장애인 추가공제."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=2,
            disabled_count=1,
        )
        # 기본(3M) + 장애인(2M) = 5M
        assert result["personal_deduction"] == 5_000_000

    def test_additional_deduction_single_parent(self):
        """한부모 추가공제."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=2,
            is_single_parent=True,
        )
        # 기본(3M) + 한부모(1M) = 4M
        assert result["personal_deduction"] == 4_000_000

    def test_additional_deduction_woman(self):
        """부녀자 추가공제."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=2,
            is_woman_deduction=True,
        )
        # 기본(3M) + 부녀자(50만) = 3,500,000
        assert result["personal_deduction"] == 3_500_000

    def test_single_parent_overrides_woman(self):
        """한부모 공제와 부녀자 공제 중복 시 한부모만 적용."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=2,
            is_single_parent=True,
            is_woman_deduction=True,
        )
        # 기본(3M) + 한부모(1M) = 4M (부녀자 중복 불가)
        assert result["personal_deduction"] == 4_000_000

    def test_insurance_income_deduction_only_health(self):
        """건강보험만 있는 경우."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=1,
            health_insurance=1_000_000,
        )
        assert result["insurance_income_deduction"] == 1_000_000

    def test_insurance_income_deduction_all(self):
        """건강 + 장기요양 + 고용보험."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=1,
            health_insurance=1_000_000,
            long_term_care=200_000,
            employment_insurance=300_000,
        )
        assert result["insurance_income_deduction"] == 1_500_000


# =============================================================================
# 세액공제 관련 검증
# =============================================================================
class TestTaxCredits:
    """세액공제 계산 검증."""

    def test_child_tax_credit_no_children(self):
        """자녀 없음: 공제 0원."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=1,
        )
        assert result["child_tax_credit"] == 0

    def test_child_tax_credit_one_over_8(self):
        """8세 이상 1명: 25만원."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=2,
            children_over_8=1,
        )
        assert result["child_tax_credit"] == 250_000

    def test_child_tax_credit_two_over_8(self):
        """8세 이상 2명: 55만원."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=3,
            children_over_8=2,
        )
        assert result["child_tax_credit"] == 550_000

    def test_child_tax_credit_birth_third(self):
        """출산 셋째: 70만원."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=2,
            birth_orders=[3],
        )
        assert result["child_tax_credit"] == 700_000

    def test_special_tax_credit_sum(self):
        """특별세액공제 = 보험+의료+교육+기부금."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=1,
            insurance_tax_credit=100_000,
            medical_tax_credit=200_000,
            education_tax_credit=300_000,
            donation_tax_credit=400_000,
        )
        assert result["special_tax_credit"] == 1_000_000


# =============================================================================
# 결정세액 및 환급 검증
# =============================================================================
class TestDeterminedTaxAndRefund:
    """결정세액 및 환급 계산."""

    def test_determined_tax_cannot_be_negative(self):
        """결정세액은 0 미만이 될 수 없음."""
        result = calc_year_end_tax(
            total_salary=30_000_000,
            num_dependents=5,
            insurance_tax_credit=5_000_000,
            medical_tax_credit=5_000_000,
        )
        assert result["determined_tax"] >= 0

    def test_refund_negative_means_refund(self):
        """환급액이 음수 = 돌려받는 금액."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=1,
            prepaid_tax=5_000_000,
        )
        # 기납부세액이 결정세액보다 크면 환급
        if result["prepaid_tax"] > result["determined_tax"]:
            assert result["refund_amount"] < 0

    def test_refund_positive_means_additional_payment(self):
        """환급액이 양수 = 추가납부 금액."""
        result = calc_year_end_tax(
            total_salary=100_000_000,
            num_dependents=1,
            prepaid_tax=0,
        )
        # 기납부세액 0이면 결정세액만큼 추가납부
        assert result["refund_amount"] == result["determined_tax"]
        assert result["refund_amount"] > 0

    def test_refund_formula(self):
        """환급액 = 결정세액 - 기납부세액."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=1,
            prepaid_tax=2_000_000,
        )
        assert result["refund_amount"] == result["determined_tax"] - result["prepaid_tax"]


# =============================================================================
# 기본값 및 순수함수 검증
# =============================================================================
class TestDefaultsAndPurity:
    """기본값 및 순수 함수 검증."""

    def test_minimal_input(self):
        """최소 입력으로도 동작."""
        result = calc_year_end_tax(
            total_salary=50_000_000,
            num_dependents=1,
        )
        assert result["total_salary"] == 50_000_000
        assert result["personal_deduction"] == 1_500_000
        assert result["pension_insurance_deduction"] == 0
        assert result["insurance_income_deduction"] == 0
        assert result["housing_deduction"] == 0
        assert result["card_deduction"] == 0
        assert result["prepaid_tax"] == 0

    def test_pure_function_same_input_same_output(self):
        """순수 함수: 동일 입력 -> 동일 출력."""
        kwargs = {
            "total_salary": 65_400_000,
            "num_dependents": 4,
            "national_pension": 2_500_000,
            "health_insurance": 1_300_000,
            "long_term_care": 400_000,
            "housing_loan_deduction": 1_000_000,
            "card_deduction": 4_895_000,
            "children_over_8": 1,
            "birth_orders": [3],
            "pension_savings": 2_000_000,
            "retirement_pension": 1_000_000,
            "insurance_tax_credit": 120_000,
            "medical_tax_credit": 950_700,
            "education_tax_credit": 630_000,
            "donation_tax_credit": 271_818,
            "prepaid_tax": 1_000_000,
        }
        result1 = calc_year_end_tax(**kwargs)
        result2 = calc_year_end_tax(**kwargs)
        assert result1 == result2

    def test_taxable_income_cannot_be_negative(self):
        """과세표준은 0 미만이 될 수 없음."""
        result = calc_year_end_tax(
            total_salary=5_000_000,
            num_dependents=10,
            national_pension=5_000_000,
            card_deduction=5_000_000,
        )
        assert result["taxable_income"] >= 0

    def test_zero_salary(self):
        """총급여 0원."""
        result = calc_year_end_tax(
            total_salary=0,
            num_dependents=1,
        )
        assert result["total_salary"] == 0
        assert result["earned_income_deduction"] == 0
        assert result["earned_income_amount"] == 0
        assert result["taxable_income"] == 0
        assert result["calculated_tax"] == 0
        assert result["determined_tax"] == 0


# =============================================================================
# 소득공제 종합한도 (조특법 제132조의2) [p.147]
# =============================================================================
class TestDeductionLimit:
    """소득공제 종합한도 검증.

    Note: 소득공제 종합한도 2,500만원은 신용카드등 + 주택마련저축 등에 적용.
    이강모 사례에서는 초과 없음.
    """

    def test_kangmo_no_excess(self):
        """이강모 사례: 종합한도 초과 없음."""
        result = calc_year_end_tax(
            total_salary=65_400_000,
            num_dependents=4,
            national_pension=2_500_000,
            health_insurance=1_300_000,
            long_term_care=400_000,
            housing_loan_deduction=1_000_000,
            card_deduction=4_895_000,
            children_over_8=1,
            birth_orders=[3],
            pension_savings=2_000_000,
            retirement_pension=1_000_000,
            insurance_tax_credit=120_000,
            medical_tax_credit=950_700,
            education_tax_credit=630_000,
            donation_tax_credit=271_818,
            prepaid_tax=1_000_000,
        )
        # card_deduction(4,895,000) + other_income_deductions(0) < 25,000,000
        assert result["card_deduction"] == 4_895_000
