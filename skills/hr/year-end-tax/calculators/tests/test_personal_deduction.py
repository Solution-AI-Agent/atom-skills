"""
Tests for personal_deduction.py - 인적공제(기본/추가) + 자녀세액공제

TDD RED phase: Write tests first, then implement.
All amounts in KRW (원).
"""

import pytest

from personal_deduction import (
    calc_basic_personal_deduction,
    calc_additional_deduction,
    calc_child_tax_credit,
)
from test_data import CASE, CHILD


# =============================================================================
# calc_basic_personal_deduction (기본공제) [p.95]
# =============================================================================
class TestCalcBasicPersonalDeduction:
    """기본공제 = 1인당 150만원 x 인원수"""

    def test_zero_dependents(self):
        """부양가족 0명"""
        assert calc_basic_personal_deduction(0) == 0

    def test_self_only(self):
        """본인 1명"""
        assert calc_basic_personal_deduction(1) == 1_500_000

    def test_two_dependents(self):
        """2명"""
        assert calc_basic_personal_deduction(2) == 3_000_000

    def test_case_kangmo(self):
        """이강모 사례: 본인 + 자녀3명 = 4명"""
        assert calc_basic_personal_deduction(4) == 6_000_000

    def test_large_family(self):
        """대가족 7명"""
        assert calc_basic_personal_deduction(7) == 10_500_000

    def test_matches_test_data(self):
        """이강모 테스트 데이터 검증"""
        assert calc_basic_personal_deduction(CASE["basic_dependents"]) == CASE["personal_deduction"]


# =============================================================================
# calc_additional_deduction (추가공제) [p.99-102]
# =============================================================================
class TestCalcAdditionalDeduction:
    """추가공제: 경로우대, 장애인, 한부모, 부녀자"""

    def test_no_additional(self):
        """추가공제 해당 없음"""
        assert calc_additional_deduction() == 0

    def test_elderly_only(self):
        """경로우대 1명: 100만원"""
        assert calc_additional_deduction(elderly_count=1) == 1_000_000

    def test_elderly_multiple(self):
        """경로우대 2명: 200만원"""
        assert calc_additional_deduction(elderly_count=2) == 2_000_000

    def test_disabled_only(self):
        """장애인 1명: 200만원"""
        assert calc_additional_deduction(disabled_count=1) == 2_000_000

    def test_disabled_multiple(self):
        """장애인 3명: 600만원"""
        assert calc_additional_deduction(disabled_count=3) == 6_000_000

    def test_single_parent(self):
        """한부모: 100만원"""
        assert calc_additional_deduction(is_single_parent=True) == 1_000_000

    def test_woman_deduction(self):
        """부녀자: 50만원"""
        assert calc_additional_deduction(is_woman_deduction=True) == 500_000

    def test_single_parent_overrides_woman(self):
        """한부모와 부녀자 중복 불가: 한부모 우선 (100만원)"""
        assert calc_additional_deduction(
            is_single_parent=True,
            is_woman_deduction=True,
        ) == 1_000_000

    def test_elderly_and_disabled(self):
        """경로우대 + 장애인 중복 가능"""
        # 1 elderly (100만) + 1 disabled (200만) = 300만
        assert calc_additional_deduction(elderly_count=1, disabled_count=1) == 3_000_000

    def test_all_combined(self):
        """경로우대 + 장애인 + 한부모 모두 해당"""
        # 1 elderly (100만) + 1 disabled (200만) + single_parent (100만) = 400만
        assert calc_additional_deduction(
            elderly_count=1,
            disabled_count=1,
            is_single_parent=True,
        ) == 4_000_000

    def test_all_combined_woman_ignored(self):
        """경로우대 + 장애인 + 한부모 + 부녀자: 한부모 우선"""
        # 1 elderly (100만) + 1 disabled (200만) + single_parent (100만) = 400만
        # 부녀자 50만은 한부모와 중복 불가로 무시
        assert calc_additional_deduction(
            elderly_count=1,
            disabled_count=1,
            is_single_parent=True,
            is_woman_deduction=True,
        ) == 4_000_000

    def test_elderly_disabled_woman(self):
        """경로우대 + 장애인 + 부녀자 (한부모 아님)"""
        # 1 elderly (100만) + 1 disabled (200만) + woman (50만) = 350만
        assert calc_additional_deduction(
            elderly_count=1,
            disabled_count=1,
            is_woman_deduction=True,
        ) == 3_500_000


# =============================================================================
# calc_child_tax_credit (자녀세액공제) [p.160-161]
# =============================================================================
class TestCalcChildTaxCredit:
    """자녀세액공제 테스트"""

    def test_no_children(self):
        """자녀 없음"""
        assert calc_child_tax_credit(0) == 0

    def test_one_child_over_8(self):
        """8세 이상 1명: 25만원"""
        assert calc_child_tax_credit(1) == 250_000

    def test_two_children_over_8(self):
        """8세 이상 2명: 55만원"""
        assert calc_child_tax_credit(2) == 550_000

    def test_three_children_over_8(self):
        """8세 이상 3명: 55만원 + 30만원 = 85만원"""
        assert calc_child_tax_credit(3) == 850_000

    def test_four_children_over_8(self):
        """8세 이상 4명: 55만원 + 30만원 x 2 = 115만원"""
        assert calc_child_tax_credit(4) == 1_150_000

    def test_birth_first_child(self):
        """출산/입양 첫째: 30만원"""
        assert calc_child_tax_credit(0, birth_orders=[1]) == 300_000

    def test_birth_second_child(self):
        """출산/입양 둘째: 50만원"""
        assert calc_child_tax_credit(0, birth_orders=[2]) == 500_000

    def test_birth_third_child(self):
        """출산/입양 셋째: 70만원"""
        assert calc_child_tax_credit(0, birth_orders=[3]) == 700_000

    def test_birth_fourth_child(self):
        """출산/입양 넷째 이상: 70만원"""
        assert calc_child_tax_credit(0, birth_orders=[4]) == 700_000

    def test_birth_multiple(self):
        """출산/입양 첫째 + 둘째"""
        assert calc_child_tax_credit(0, birth_orders=[1, 2]) == 800_000

    def test_case_kangmo(self):
        """이강모 사례: 8세이상 1명 + 출산 셋째"""
        # 250_000 + 700_000 = 950_000
        assert calc_child_tax_credit(1, birth_orders=[3]) == 950_000

    def test_over_8_and_births_combined(self):
        """8세이상 2명 + 출산 둘째"""
        # 550_000 + 500_000 = 1_050_000
        assert calc_child_tax_credit(2, birth_orders=[2]) == 1_050_000

    def test_empty_birth_orders(self):
        """출산 리스트가 빈 리스트인 경우"""
        assert calc_child_tax_credit(1, birth_orders=[]) == 250_000

    def test_none_birth_orders(self):
        """출산 리스트가 None인 경우"""
        assert calc_child_tax_credit(1, birth_orders=None) == 250_000

    def test_matches_test_data(self):
        """이강모 테스트 데이터 검증"""
        assert calc_child_tax_credit(
            CHILD["children_over_8"],
            birth_orders=[CHILD["birth_order"]],
        ) == CHILD["total_credit"]
