"""
교육비 세액공제 계산기 테스트 [p.177-186]

TDD: RED phase - 테스트를 먼저 작성합니다.
"""
from education_deduction import (
    calc_education_tax_credit,
)
from test_data import CASE, EDUCATION


# =============================================================================
# calc_education_tax_credit (교육비 세액공제)
# =============================================================================
class TestEducationTaxCredit:
    """교육비 세액공제 15% [p.177-186]."""

    def test_case_kangmo(self):
        """이강모 사례: 취학전 120만 + 고등학생 300만(한도) = 420만 x 15% = 63만."""
        result = calc_education_tax_credit(
            self_education=EDUCATION["self_eligible"],
            preschool_amounts=[EDUCATION["preschool_gym"]],
            school_amounts=[
                EDUCATION["highschool_tuition"]
                + EDUCATION["highschool_uniform"]
                + 300_000  # 체험학습 한도 30만
                + EDUCATION["highschool_sat"]
            ],
        )
        assert result == EDUCATION["tax_credit"]
        assert result == 630_000

    def test_self_education_no_limit(self):
        """본인 교육비는 한도 없이 전액 공제."""
        result = calc_education_tax_credit(self_education=50_000_000)
        assert result == int(50_000_000 * 0.15)

    def test_self_education_large_amount(self):
        """본인 교육비 1억원 - 한도 없음 확인."""
        result = calc_education_tax_credit(self_education=100_000_000)
        assert result == int(100_000_000 * 0.15)

    def test_preschool_within_limit(self):
        """취학전 아동 1인, 한도 300만원 이내."""
        result = calc_education_tax_credit(preschool_amounts=[2_000_000])
        assert result == int(2_000_000 * 0.15)

    def test_preschool_exceeds_limit(self):
        """취학전 아동 1인, 한도 300만원 초과."""
        result = calc_education_tax_credit(preschool_amounts=[5_000_000])
        assert result == int(3_000_000 * 0.15)

    def test_preschool_at_limit(self):
        """취학전 아동 1인, 정확히 300만원."""
        result = calc_education_tax_credit(preschool_amounts=[3_000_000])
        assert result == int(3_000_000 * 0.15)

    def test_preschool_multiple_children(self):
        """취학전 아동 3명 - 각각 개별 한도 적용."""
        result = calc_education_tax_credit(
            preschool_amounts=[2_000_000, 4_000_000, 1_000_000]
        )
        # child1: 200만 (한도내), child2: 300만 (한도), child3: 100만 (한도내)
        expected = int((2_000_000 + 3_000_000 + 1_000_000) * 0.15)
        assert result == expected

    def test_school_within_limit(self):
        """초중고 학생 1인, 한도 300만원 이내."""
        result = calc_education_tax_credit(school_amounts=[2_500_000])
        assert result == int(2_500_000 * 0.15)

    def test_school_exceeds_limit(self):
        """초중고 학생 1인, 한도 300만원 초과."""
        result = calc_education_tax_credit(school_amounts=[4_000_000])
        assert result == int(3_000_000 * 0.15)

    def test_school_multiple_students(self):
        """초중고 학생 2명 - 각각 개별 한도."""
        result = calc_education_tax_credit(
            school_amounts=[3_500_000, 1_500_000]
        )
        # student1: 300만 (한도), student2: 150만 (한도내)
        expected = int((3_000_000 + 1_500_000) * 0.15)
        assert result == expected

    def test_university_within_limit(self):
        """대학생 1인, 한도 900만원 이내."""
        result = calc_education_tax_credit(university_amounts=[7_000_000])
        assert result == int(7_000_000 * 0.15)

    def test_university_exceeds_limit(self):
        """대학생 1인, 한도 900만원 초과."""
        result = calc_education_tax_credit(university_amounts=[12_000_000])
        assert result == int(9_000_000 * 0.15)

    def test_university_at_limit(self):
        """대학생 1인, 정확히 900만원."""
        result = calc_education_tax_credit(university_amounts=[9_000_000])
        assert result == int(9_000_000 * 0.15)

    def test_university_multiple_students(self):
        """대학생 2명 - 각각 개별 한도."""
        result = calc_education_tax_credit(
            university_amounts=[10_000_000, 5_000_000]
        )
        # student1: 900만 (한도), student2: 500만 (한도내)
        expected = int((9_000_000 + 5_000_000) * 0.15)
        assert result == expected

    def test_disabled_special_no_limit(self):
        """장애인 특수교육비는 한도 없이 전액 공제."""
        result = calc_education_tax_credit(disabled_special=20_000_000)
        assert result == int(20_000_000 * 0.15)

    def test_all_categories_combined(self):
        """모든 카테고리 복합."""
        result = calc_education_tax_credit(
            self_education=10_000_000,
            preschool_amounts=[2_000_000, 4_000_000],
            school_amounts=[3_500_000],
            university_amounts=[10_000_000],
            disabled_special=5_000_000,
        )
        # self: 1000만, preschool: 200만+300만=500만
        # school: 300만(한도), university: 900만(한도)
        # disabled: 500만
        total_eligible = 10_000_000 + 5_000_000 + 3_000_000 + 9_000_000 + 5_000_000
        expected = int(total_eligible * 0.15)
        assert result == expected

    def test_zero_all(self):
        """모든 금액이 0인 경우."""
        result = calc_education_tax_credit()
        assert result == 0

    def test_zero_amounts_in_lists(self):
        """리스트 내 0원 항목."""
        result = calc_education_tax_credit(
            preschool_amounts=[0, 0],
            school_amounts=[0],
        )
        assert result == 0

    def test_empty_lists(self):
        """빈 리스트 전달."""
        result = calc_education_tax_credit(
            preschool_amounts=[],
            school_amounts=[],
            university_amounts=[],
        )
        assert result == 0

    def test_none_lists_default(self):
        """리스트 기본값 None."""
        result = calc_education_tax_credit(self_education=1_000_000)
        assert result == int(1_000_000 * 0.15)

    def test_boundary_one_won(self):
        """1원 경계값 - 소수점 이하 절삭."""
        result = calc_education_tax_credit(self_education=1)
        # 1 x 0.15 = 0.15 -> int(0) = 0
        assert result == 0

    def test_boundary_seven_won(self):
        """7원 경계값 - 소수점 이하 절삭 확인."""
        result = calc_education_tax_credit(self_education=7)
        # 7 x 0.15 = 1.05 -> int(1) = 1
        assert result == 1

    def test_single_preschool_child(self):
        """취학전 아동 1명만 있는 경우."""
        result = calc_education_tax_credit(
            preschool_amounts=[1_200_000],
        )
        assert result == int(1_200_000 * 0.15)
        assert result == 180_000
