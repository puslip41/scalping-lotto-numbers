"""
LottoData 모델 테스트
"""

import pytest
from models import LottoData


class TestLottoData:
    """LottoData 모델 테스트 클래스"""
    
    def test_valid_lotto_data(self):
        """유효한 로또 데이터 생성 테스트"""
        data = LottoData(
            round_num=1,
            draw_date='2002-12-07',
            winning_numbers=[10, 23, 29, 33, 37, 40],
            bonus_number=16,
            first_prize_winners=4,
            first_prize_amount=2067000000
        )
        
        assert data.round_num == 1
        assert data.draw_date == '2002-12-07'
        assert data.winning_numbers == [10, 23, 29, 33, 37, 40]
        assert data.bonus_number == 16
        assert data.first_prize_winners == 4
        assert data.first_prize_amount == 2067000000
    
    def test_invalid_winning_numbers_count(self):
        """잘못된 당첨번호 개수 테스트"""
        with pytest.raises(ValueError, match="당첨번호는 6개여야 합니다"):
            LottoData(
                round_num=1,
                draw_date='2002-12-07',
                winning_numbers=[10, 23, 29],  # 3개만
                bonus_number=16,
                first_prize_winners=4,
                first_prize_amount=2067000000
            )
    
    def test_invalid_number_range(self):
        """잘못된 번호 범위 테스트"""
        with pytest.raises(ValueError, match="당첨번호는 1-45 범위여야 합니다"):
            LottoData(
                round_num=1,
                draw_date='2002-12-07',
                winning_numbers=[10, 23, 29, 33, 37, 50],  # 50은 범위 밖
                bonus_number=16,
                first_prize_winners=4,
                first_prize_amount=2067000000
            )
    
    def test_duplicate_winning_numbers(self):
        """중복된 당첨번호 테스트"""
        with pytest.raises(ValueError, match="당첨번호에 중복이 있습니다"):
            LottoData(
                round_num=1,
                draw_date='2002-12-07',
                winning_numbers=[10, 23, 29, 33, 37, 10],  # 10 중복
                bonus_number=16,
                first_prize_winners=4,
                first_prize_amount=2067000000
            )
    
    def test_bonus_number_duplicate_with_winning(self):
        """보너스번호와 당첨번호 중복 테스트"""
        with pytest.raises(ValueError, match="보너스번호는 당첨번호와 중복될 수 없습니다"):
            LottoData(
                round_num=1,
                draw_date='2002-12-07',
                winning_numbers=[10, 23, 29, 33, 37, 40],
                bonus_number=10,  # 당첨번호와 중복
                first_prize_winners=4,
                first_prize_amount=2067000000
            )
    
    def test_invalid_date_format(self):
        """잘못된 날짜 형식 테스트"""
        with pytest.raises(ValueError, match="날짜 형식이 올바르지 않습니다"):
            LottoData(
                round_num=1,
                draw_date='2002/12/07',  # 잘못된 형식
                winning_numbers=[10, 23, 29, 33, 37, 40],
                bonus_number=16,
                first_prize_winners=4,
                first_prize_amount=2067000000
            )
    
    def test_to_dict(self):
        """딕셔너리 변환 테스트"""
        data = LottoData(
            round_num=1,
            draw_date='2002-12-07',
            winning_numbers=[10, 23, 29, 33, 37, 40],
            bonus_number=16,
            first_prize_winners=4,
            first_prize_amount=2067000000
        )
        
        result = data.to_dict()
        
        expected = {
            '회차': 1,
            '추첨일': '2002-12-07',
            '당첨번호1': 10,
            '당첨번호2': 23,
            '당첨번호3': 29,
            '당첨번호4': 33,
            '당첨번호5': 37,
            '당첨번호6': 40,
            '보너스번호': 16,
            '1등당첨자수': 4,
            '1등당첨금액': 2067000000
        }
        
        assert result == expected
