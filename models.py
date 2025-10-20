"""
로또 데이터 모델
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class LottoData:
    """로또 당첨 데이터 모델"""
    round_num: int
    draw_date: str
    winning_numbers: List[int]
    bonus_number: int
    first_prize_winners: int
    first_prize_amount: int
    
    def __post_init__(self):
        """데이터 검증"""
        self._validate_numbers()
        self._validate_date()
        self._validate_amounts()
    
    def _validate_numbers(self):
        """당첨번호 및 보너스번호 검증"""
        # 당첨번호 검증
        if len(self.winning_numbers) != 6:
            raise ValueError(f"당첨번호는 6개여야 합니다. 현재: {len(self.winning_numbers)}개")
        
        for num in self.winning_numbers:
            if not (1 <= num <= 45):
                raise ValueError(f"당첨번호는 1-45 범위여야 합니다. 현재: {num}")
        
        # 보너스번호 검증
        if not (1 <= self.bonus_number <= 45):
            raise ValueError(f"보너스번호는 1-45 범위여야 합니다. 현재: {self.bonus_number}")
        
        # 당첨번호와 보너스번호 중복 검사
        if self.bonus_number in self.winning_numbers:
            raise ValueError(f"보너스번호는 당첨번호와 중복될 수 없습니다. 보너스번호: {self.bonus_number}")
        
        # 당첨번호 중복 검사
        if len(set(self.winning_numbers)) != len(self.winning_numbers):
            raise ValueError("당첨번호에 중복이 있습니다.")
    
    def _validate_date(self):
        """날짜 형식 검증"""
        try:
            datetime.strptime(self.draw_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"날짜 형식이 올바르지 않습니다. 예상: YYYY-MM-DD, 현재: {self.draw_date}")
    
    def _validate_amounts(self):
        """금액 및 당첨자수 검증"""
        if self.first_prize_winners < 0:
            raise ValueError(f"1등 당첨자수는 0 이상이어야 합니다. 현재: {self.first_prize_winners}")
        
        if self.first_prize_amount < 0:
            raise ValueError(f"1등 당첨금액은 0 이상이어야 합니다. 현재: {self.first_prize_amount}")
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            '회차': self.round_num,
            '추첨일': self.draw_date,
            '당첨번호1': self.winning_numbers[0],
            '당첨번호2': self.winning_numbers[1],
            '당첨번호3': self.winning_numbers[2],
            '당첨번호4': self.winning_numbers[3],
            '당첨번호5': self.winning_numbers[4],
            '당첨번호6': self.winning_numbers[5],
            '보너스번호': self.bonus_number,
            '1등당첨자수': self.first_prize_winners,
            '1등당첨금액': self.first_prize_amount
        }
