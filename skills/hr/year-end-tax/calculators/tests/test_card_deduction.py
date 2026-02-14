"""
신용카드 등 소득공제 계산기 테스트 [p.131-147]

TDD: RED phase - 테스트를 먼저 작성합니다.
"""
from card_deduction import (
    calc_card_deduction,
)
from test_data import CASE, CARD_USAGE


# =============================================================================
# 이강모 종합사례 [p.215-216]
# =============================================================================
class TestCardDeductionKangmoCase:
    """이강모 사례를 통한 신용카드 등 소득공제 검증."""

    def test_case_kangmo_full(self):
        """이강모 사례: 총 공제 4,895,000원.

        Input:
          total_salary = 65,400,000
          credit_card = 13,000,000 (신용카드 1,500만 - 대중교통 200만)
          debit_cash = 12,000,000 (현금영수증 700만 + 체크카드 500만)
          culture = 1,000,000 (체크카드 문화체육)
          traditional = 3,000,000 (현금영수증 전통시장)
          transit = 2,000,000 (신용카드 대중교통)

        계산:
          최저사용금액 = 65,400,000 x 25% = 16,350,000
          총사용액 = 13M + 12M + 1M + 3M + 2M = 31,000,000 > 16,350,000

          공제 가능금액:
            신용카드: 13,000,000 x 15% = 1,950,000
            체크/현금: 12,000,000 x 30% = 3,600,000
            문화체육: 1,000,000 x 30% = 300,000
            전통시장: 3,000,000 x 40% = 1,200,000
            대중교통: 2,000,000 x 40% = 800,000
            소계 = 7,850,000

          최저사용금액 차감:
            신용카드(13M) x 15% = 1,950,000
            잔여(3,350,000) x 30% = 1,005,000
            차감 합계 = 2,955,000

          공제 가능금액 = 7,850,000 - 2,955,000 = 4,895,000
          기본 한도 = min(65,400,000 x 20%, 3,000,000) = 3,000,000
          추가 공제 = min(4,895,000-3,000,000, 300,000+1,200,000+800,000, 3,000,000)
                    = min(1,895,000, 2,300,000, 3,000,000) = 1,895,000
          총 공제 = 3,000,000 + 1,895,000 = 4,895,000
        """
        result = calc_card_deduction(
            total_salary=65_400_000,
            credit_card=13_000_000,
            debit_cash=12_000_000,
            culture=1_000_000,
            traditional=3_000_000,
            transit=2_000_000,
        )
        assert result == CASE["card_deduction"]
        assert result == 4_895_000


# =============================================================================
# 최저사용금액 검증
# =============================================================================
class TestMinimumUsageThreshold:
    """최저사용금액 (총급여의 25%) 관련 테스트."""

    def test_total_usage_below_minimum(self):
        """총 사용액이 최저사용금액 미만이면 공제 0원."""
        # 총급여 40M -> 최저사용금액 10M
        # 총사용액 = 5M + 3M = 8M < 10M
        result = calc_card_deduction(
            total_salary=40_000_000,
            credit_card=5_000_000,
            debit_cash=3_000_000,
        )
        assert result == 0

    def test_total_usage_exactly_at_minimum(self):
        """총 사용액이 최저사용금액과 정확히 같으면 공제 0원."""
        # 총급여 40M -> 최저사용금액 10M
        # 총사용액 = 10M
        result = calc_card_deduction(
            total_salary=40_000_000,
            credit_card=10_000_000,
            debit_cash=0,
        )
        assert result == 0

    def test_total_usage_barely_exceeds_minimum(self):
        """총 사용액이 최저사용금액을 1원 초과."""
        # 총급여 4M -> 최저사용금액 1M
        # 총사용액 = 1,000,001
        # 신용카드 1,000,001 x 15% = 150,000.15
        # 최저 차감: 1,000,000 x 15% = 150,000
        # net = 150,000.15 - 150,000 = 0.15 -> int(0) = 0
        result = calc_card_deduction(
            total_salary=4_000_000,
            credit_card=1_000_001,
            debit_cash=0,
        )
        assert result == 0

    def test_zero_total_salary(self):
        """총급여 0원이면 최저사용금액도 0원."""
        # 최저사용금액 = 0, 사용액 1M > 0
        # 신용카드 1M x 15% = 150,000
        # 최저 차감 = 0
        # net = 150,000
        # 기본 한도 = min(0 x 20%, 3M) = 0
        result = calc_card_deduction(
            total_salary=0,
            credit_card=1_000_000,
            debit_cash=0,
        )
        assert result == 0


# =============================================================================
# 결제수단별 공제율 검증
# =============================================================================
class TestDeductionRates:
    """결제수단별 공제율 적용 검증."""

    def test_credit_card_15_percent(self):
        """신용카드 15% 공제율."""
        # 총급여 100M -> 최저 25M, 한도 250만
        # 신용카드 30M -> gross = 30M x 15% = 4,500,000
        # 최저차감 = 25M x 15% = 3,750,000
        # net = 750,000
        # 기본 한도(100M초과) = 2,500,000
        # 공제 = min(750,000, 2,500,000) = 750,000
        result = calc_card_deduction(
            total_salary=100_000_000,
            credit_card=30_000_000,
            debit_cash=0,
        )
        assert result == 750_000

    def test_debit_cash_30_percent(self):
        """체크카드/현금영수증 30% 공제율."""
        # 총급여 20M -> 최저 5M
        # 체크카드 10M -> gross = 10M x 30% = 3,000,000
        # 최저차감 = 5M x 30% = 1,500,000
        # net = 1,500,000
        # 기본 한도 = min(20M x 20%, 3M) = min(4M, 3M) = 3M
        # 공제 = min(1,500,000, 3,000,000) = 1,500,000
        result = calc_card_deduction(
            total_salary=20_000_000,
            credit_card=0,
            debit_cash=10_000_000,
        )
        assert result == 1_500_000

    def test_traditional_market_40_percent(self):
        """전통시장 40% 공제율."""
        # 총급여 20M -> 최저 5M
        # 전통시장 10M -> gross = 10M x 40% = 4,000,000
        # 최저차감 = 5M x 40% = 2,000,000
        # net = 2,000,000
        # 기본 한도 = min(4M, 3M) = 3M
        # 기본 = min(2M, 3M) = 2M
        # 추가(전통시장) = min(0, 2M, 3M) = 0 (excess=0)
        result = calc_card_deduction(
            total_salary=20_000_000,
            credit_card=0,
            debit_cash=0,
            traditional=10_000_000,
        )
        assert result == 2_000_000

    def test_transit_40_percent(self):
        """대중교통 40% 공제율."""
        # 총급여 20M -> 최저 5M
        # 대중교통 10M -> gross = 10M x 40% = 4,000,000
        # 최저차감 = 5M x 40% = 2,000,000
        # net = 2,000,000
        result = calc_card_deduction(
            total_salary=20_000_000,
            credit_card=0,
            debit_cash=0,
            transit=10_000_000,
        )
        assert result == 2_000_000

    def test_culture_30_percent_under_70m(self):
        """문화체육 30% 공제율 (총급여 7천만원 이하)."""
        # 총급여 60M -> 최저 15M
        # 문화체육 20M -> gross = 20M x 30% = 6,000,000
        # 최저차감 = 15M x 30% = 4,500,000
        # net = 1,500,000
        # 기본 한도 = min(60M x 20%, 3M) = 3M
        # 기본 = min(1,500,000, 3M) = 1,500,000
        result = calc_card_deduction(
            total_salary=60_000_000,
            credit_card=0,
            debit_cash=0,
            culture=20_000_000,
        )
        assert result == 1_500_000

    def test_culture_ignored_over_70m(self):
        """문화체육: 총급여 7천만원 초과시 공제 대상 아님."""
        # 총급여 80M -> 최저 20M
        # 신용카드 25M (최저 충족용) + 문화체육 5M
        # 문화체육은 7천만원 초과이므로 0% 처리
        # 신용카드: 25M x 15% = 3,750,000
        # 최저차감: 20M x 15% = 3,000,000
        # net = 750,000
        # 기본 한도(80M>70M) = 2,500,000
        # 공제 = min(750,000, 2,500,000) = 750,000
        result = calc_card_deduction(
            total_salary=80_000_000,
            credit_card=25_000_000,
            debit_cash=0,
            culture=5_000_000,
        )
        assert result == 750_000


# =============================================================================
# 기본 공제 한도 검증
# =============================================================================
class TestBasicLimit:
    """기본 공제 한도 적용 검증."""

    def test_limit_under_70m_capped_at_3m(self):
        """7천만원 이하: min(총급여x20%, 300만원) -> 300만원 cap."""
        # 총급여 60M -> 최저 15M
        # 한도 = min(60M x 20%, 3M) = min(12M, 3M) = 3M
        # 체크카드 30M -> gross = 30M x 30% = 9M
        # 최저차감 = 15M x 30% = 4.5M
        # net = 4.5M > 3M -> capped at 3M (basic)
        result = calc_card_deduction(
            total_salary=60_000_000,
            credit_card=0,
            debit_cash=30_000_000,
        )
        assert result == 3_000_000

    def test_limit_under_70m_salary_rate_lower(self):
        """7천만원 이하: min(총급여x20%, 300만원) -> 총급여x20%가 더 작은 경우."""
        # 총급여 10M -> 최저 2.5M
        # 한도 = min(10M x 20%, 3M) = min(2M, 3M) = 2M
        # 체크카드 10M -> gross = 10M x 30% = 3M
        # 최저차감 = 2.5M x 30% = 750,000
        # net = 2,250,000 > 2M -> capped at 2M (basic)
        result = calc_card_deduction(
            total_salary=10_000_000,
            credit_card=0,
            debit_cash=10_000_000,
        )
        assert result == 2_000_000

    def test_limit_over_70m(self):
        """7천만원 초과: 250만원 한도."""
        # 총급여 80M -> 최저 20M, 한도 250만
        # 체크카드 30M -> gross = 30M x 30% = 9M
        # 최저차감 = 20M x 30% = 6M
        # net = 3M > 2.5M -> capped at 2.5M
        result = calc_card_deduction(
            total_salary=80_000_000,
            credit_card=0,
            debit_cash=30_000_000,
        )
        assert result == 2_500_000

    def test_limit_exactly_70m(self):
        """총급여 정확히 7천만원: 이하 기준 적용."""
        # 총급여 70M -> 최저 17.5M
        # 한도 = min(70M x 20%, 3M) = min(14M, 3M) = 3M
        # 체크카드 30M -> gross = 30M x 30% = 9M
        # 최저차감 = 17.5M x 30% = 5.25M
        # net = 3.75M > 3M -> capped at 3M
        result = calc_card_deduction(
            total_salary=70_000_000,
            credit_card=0,
            debit_cash=30_000_000,
        )
        assert result == 3_000_000


# =============================================================================
# 추가 공제 검증
# =============================================================================
class TestAdditionalDeduction:
    """추가 공제 (문화체육+전통시장+대중교통) 검증."""

    def test_additional_deduction_from_traditional_and_transit(self):
        """기본 한도 초과시 전통시장+대중교통으로 추가 공제."""
        # 총급여 40M -> 최저 10M
        # 한도 = min(40M x 20%, 3M) = min(8M, 3M) = 3M
        # 체크카드 20M, 전통시장 5M, 대중교통 3M
        # 최저차감: 체크(10M) x 30% = (wait, no credit_card first)
        # Actually minimum subtracted from credit first, then debit...
        # credit=0, debit=20M, trad=5M, transit=3M
        # min_remaining = 10M
        # credit(0): consumed=0, remaining=10M
        # debit(20M): consumed=10M, net=10M, remaining=0
        # trad(5M): consumed=0, net=5M
        # transit(3M): consumed=0, net=3M
        #
        # net_deductions:
        #   credit: 0
        #   debit: 10M x 30% = 3M
        #   trad: 5M x 40% = 2M
        #   transit: 3M x 40% = 1.2M
        # net_total = 6.2M
        #
        # basic = min(6.2M, 3M) = 3M
        # excess = 3.2M
        # additional_sources = 0(culture) + 2M(trad) + 1.2M(transit) = 3.2M
        # additional_limit = 3M (under 70M)
        # additional = min(3.2M, 3.2M, 3M) = 3M
        # total = 3M + 3M = 6M
        result = calc_card_deduction(
            total_salary=40_000_000,
            credit_card=0,
            debit_cash=20_000_000,
            traditional=5_000_000,
            transit=3_000_000,
        )
        assert result == 6_000_000

    def test_additional_limit_300m_under_70m(self):
        """7천만원 이하: 추가 공제 한도 300만원."""
        # 총급여 40M -> 최저 10M
        # 체크카드 20M, 전통시장 20M
        # min_remaining=10M -> debit: consumed=10M, net=10M
        # net_deductions:
        #   debit: 10M x 30% = 3M
        #   trad: 20M x 40% = 8M
        # net_total = 11M
        # basic = 3M, excess = 8M
        # additional_sources = 8M
        # additional = min(8M, 8M, 3M) = 3M
        # total = 3M + 3M = 6M
        result = calc_card_deduction(
            total_salary=40_000_000,
            credit_card=0,
            debit_cash=20_000_000,
            traditional=20_000_000,
        )
        assert result == 6_000_000

    def test_additional_limit_200m_over_70m(self):
        """7천만원 초과: 추가 공제 한도 200만원."""
        # 총급여 80M -> 최저 20M, 기본한도 2.5M
        # 체크카드 30M, 전통시장 10M
        # min_remaining=20M -> debit: consumed=20M, net=10M
        # net_deductions:
        #   debit: 10M x 30% = 3M
        #   trad: 10M x 40% = 4M
        # net_total = 7M
        # basic = min(7M, 2.5M) = 2.5M, excess = 4.5M
        # additional_sources = 4M
        # additional_limit = 2M (over 70M)
        # additional = min(4.5M, 4M, 2M) = 2M
        # total = 2.5M + 2M = 4.5M
        result = calc_card_deduction(
            total_salary=80_000_000,
            credit_card=0,
            debit_cash=30_000_000,
            traditional=10_000_000,
        )
        assert result == 4_500_000

    def test_no_additional_when_under_basic_limit(self):
        """net이 기본 한도 이내면 추가 공제 없음."""
        # 총급여 40M -> 최저 10M, 한도 3M
        # 신용카드 15M -> gross = 15M x 15% = 2.25M
        # 최저차감: 10M x 15% = 1.5M
        # net = 750,000 < 3M -> no additional
        result = calc_card_deduction(
            total_salary=40_000_000,
            credit_card=15_000_000,
            debit_cash=0,
        )
        assert result == 750_000

    def test_additional_capped_by_excess(self):
        """추가 공제가 초과액에 의해 제한."""
        # net_total - basic_limit < additional_sources인 경우
        # 이강모 사례가 이에 해당: excess 1,895,000 < sources 2,300,000
        result = calc_card_deduction(
            total_salary=65_400_000,
            credit_card=13_000_000,
            debit_cash=12_000_000,
            culture=1_000_000,
            traditional=3_000_000,
            transit=2_000_000,
        )
        assert result == 4_895_000


# =============================================================================
# 최저사용금액 차감 순서 검증
# =============================================================================
class TestMinimumSubtractionOrder:
    """최저사용금액은 신용카드부터 우선 차감."""

    def test_minimum_fully_from_credit_card(self):
        """최저사용금액이 신용카드로 완전히 충당."""
        # 총급여 20M -> 최저 5M
        # 신용카드 10M, 체크카드 5M
        # 최저차감: credit(5M) x 15% = 750,000
        # net_deductions:
        #   credit: (10M-5M) x 15% = 750,000
        #   debit: 5M x 30% = 1,500,000
        # net_total = 2,250,000
        # 한도 = min(4M, 3M) = 3M
        # 공제 = min(2,250,000, 3M) = 2,250,000
        result = calc_card_deduction(
            total_salary=20_000_000,
            credit_card=10_000_000,
            debit_cash=5_000_000,
        )
        assert result == 2_250_000

    def test_minimum_overflows_to_debit(self):
        """최저사용금액이 신용카드를 초과하여 체크카드로 이월."""
        # 총급여 20M -> 최저 5M
        # 신용카드 3M, 체크카드 10M
        # 최저차감: credit(3M) x 15% = 450,000, remaining=2M
        #          debit(2M) x 30% = 600,000
        # net_deductions:
        #   credit: 0
        #   debit: (10M-2M) x 30% = 2,400,000
        # net_total = 2,400,000
        # 한도 = min(4M, 3M) = 3M
        # 공제 = min(2,400,000, 3M) = 2,400,000
        result = calc_card_deduction(
            total_salary=20_000_000,
            credit_card=3_000_000,
            debit_cash=10_000_000,
        )
        assert result == 2_400_000

    def test_minimum_overflows_to_traditional(self):
        """최저사용금액이 신용카드+체크카드를 초과하여 전통시장으로 이월."""
        # 총급여 40M -> 최저 10M
        # 신용카드 3M, 체크카드 3M, 전통시장 10M
        # 최저차감: credit(3M): 3M consumed, remaining=7M
        #          debit(3M): 3M consumed, remaining=4M
        #          trad(4M): 4M consumed, remaining=0
        # net_deductions:
        #   credit: 0
        #   debit: 0
        #   trad: (10M-4M) x 40% = 2,400,000
        # net_total = 2,400,000
        # 한도 = min(8M, 3M) = 3M
        # basic = min(2.4M, 3M) = 2.4M
        # additional: sources=2.4M, excess=0 -> 0
        result = calc_card_deduction(
            total_salary=40_000_000,
            credit_card=3_000_000,
            debit_cash=3_000_000,
            traditional=10_000_000,
        )
        assert result == 2_400_000


# =============================================================================
# 경계값 및 특수 케이스
# =============================================================================
class TestEdgeCases:
    """경계값 및 특수 케이스 검증."""

    def test_all_zero_amounts(self):
        """모든 사용액 0원."""
        result = calc_card_deduction(
            total_salary=50_000_000,
            credit_card=0,
            debit_cash=0,
        )
        assert result == 0

    def test_only_defaults(self):
        """선택 파라미터 기본값 사용."""
        result = calc_card_deduction(
            total_salary=20_000_000,
            credit_card=0,
            debit_cash=10_000_000,
        )
        # 최저 5M, debit 10M -> net 5M x 30% = 1.5M
        # 한도 = min(4M, 3M) = 3M
        assert result == 1_500_000

    def test_all_categories_combined(self):
        """모든 카테고리 동시 사용."""
        # 총급여 50M -> 최저 12.5M
        # 신용카드 10M, 체크카드 5M, 문화 2M, 전통 3M, 대중교통 3M
        # total = 23M > 12.5M
        # 최저차감: credit(10M) consumed, remaining=2.5M
        #          debit(2.5M) consumed, remaining=0
        # net_deductions:
        #   credit: 0
        #   debit: 2.5M x 30% = 750,000
        #   culture: 2M x 30% = 600,000
        #   trad: 3M x 40% = 1,200,000
        #   transit: 3M x 40% = 1,200,000
        # net_total = 3,750,000
        # 한도 = min(10M, 3M) = 3M
        # basic = 3M, excess = 750,000
        # additional_sources = 600,000 + 1,200,000 + 1,200,000 = 3M
        # additional = min(750,000, 3M, 3M) = 750,000
        # total = 3M + 750,000 = 3,750,000
        result = calc_card_deduction(
            total_salary=50_000_000,
            credit_card=10_000_000,
            debit_cash=5_000_000,
            culture=2_000_000,
            traditional=3_000_000,
            transit=3_000_000,
        )
        assert result == 3_750_000

    def test_high_salary_120m(self):
        """고소득자 1.2억: 기본한도 250만, 추가한도 200만."""
        # 총급여 120M -> 최저 30M, 기본한도 2.5M, 추가한도 2M
        # 체크카드 50M, 전통시장 10M
        # 최저: debit(30M) consumed, remaining=0
        # net_deductions:
        #   debit: 20M x 30% = 6M
        #   trad: 10M x 40% = 4M
        # net_total = 10M
        # basic = 2.5M, excess = 7.5M
        # additional = min(7.5M, 4M, 2M) = 2M
        # total = 2.5M + 2M = 4.5M
        result = calc_card_deduction(
            total_salary=120_000_000,
            credit_card=0,
            debit_cash=50_000_000,
            traditional=10_000_000,
        )
        assert result == 4_500_000

    def test_result_is_integer(self):
        """결과는 항상 정수(원)."""
        result = calc_card_deduction(
            total_salary=65_400_000,
            credit_card=13_000_000,
            debit_cash=12_000_000,
            culture=1_000_000,
            traditional=3_000_000,
            transit=2_000_000,
        )
        assert isinstance(result, int)

    def test_pure_function_no_side_effects(self):
        """순수 함수: 동일 입력 -> 동일 출력."""
        kwargs = {
            "total_salary": 65_400_000,
            "credit_card": 13_000_000,
            "debit_cash": 12_000_000,
            "culture": 1_000_000,
            "traditional": 3_000_000,
            "transit": 2_000_000,
        }
        result1 = calc_card_deduction(**kwargs)
        result2 = calc_card_deduction(**kwargs)
        assert result1 == result2
