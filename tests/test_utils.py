"""
유틸리티 함수 테스트
"""

import pytest
from utils import (
    clean_number_string, parse_date_string, validate_winning_numbers,
    validate_bonus_number, safe_int, safe_float
)


class TestUtils:
    """유틸리티 함수 테스트 클래스"""
    
    def test_clean_number_string(self):
        """숫자 문자열 정리 테스트"""
        assert clean_number_string("1,234,567") == 1234567
        assert clean_number_string("1,234") == 1234
        assert clean_number_string("123") == 123
        assert clean_number_string("") == 0
        assert clean_number_string(None) == 0
        assert clean_number_string("abc123def") == 123
    
    def test_parse_date_string(self):
        """날짜 문자열 파싱 테스트"""
        assert parse_date_string("2024.12.19") == "2024-12-19"
        assert parse_date_string("2024-12-19") == "2024-12-19"
        assert parse_date_string("2024/12/19") == "2024-12-19"
        assert parse_date_string("2024.1.1") == "2024-01-01"
        assert parse_date_string("") == ""
        assert parse_date_string("invalid") == "invalid"
    
    def test_validate_winning_numbers(self):
        """당첨번호 유효성 검사 테스트"""
        # 유효한 번호
        assert validate_winning_numbers([1, 2, 3, 4, 5, 6]) == True
        assert validate_winning_numbers([45, 44, 43, 42, 41, 40]) == True
        
        # 잘못된 개수
        assert validate_winning_numbers([1, 2, 3, 4, 5]) == False  # 5개
        assert validate_winning_numbers([1, 2, 3, 4, 5, 6, 7]) == False  # 7개
        
        # 범위 밖 번호
        assert validate_winning_numbers([0, 1, 2, 3, 4, 5]) == False  # 0 포함
        assert validate_winning_numbers([1, 2, 3, 4, 5, 46]) == False  # 46 포함
        
        # 중복 번호
        assert validate_winning_numbers([1, 1, 2, 3, 4, 5]) == False  # 1 중복
    
    def test_validate_bonus_number(self):
        """보너스번호 유효성 검사 테스트"""
        winning_numbers = [1, 2, 3, 4, 5, 6]
        
        # 유효한 보너스번호
        assert validate_bonus_number(7, winning_numbers) == True
        assert validate_bonus_number(45, winning_numbers) == True
        
        # 범위 밖 번호
        assert validate_bonus_number(0, winning_numbers) == False
        assert validate_bonus_number(46, winning_numbers) == False
        
        # 당첨번호와 중복
        assert validate_bonus_number(1, winning_numbers) == False
        assert validate_bonus_number(6, winning_numbers) == False
    
    def test_safe_int(self):
        """안전한 정수 변환 테스트"""
        assert safe_int("123") == 123
        assert safe_int("123.45") == 123
        assert safe_int("") == 0
        assert safe_int(None) == 0
        assert safe_int("abc") == 0
        assert safe_int("123", default=999) == 123
        assert safe_int("", default=999) == 999
    
    def test_safe_float(self):
        """안전한 실수 변환 테스트"""
        assert safe_float("123.45") == 123.45
        assert safe_float("123") == 123.0
        assert safe_float("") == 0.0
        assert safe_float(None) == 0.0
        assert safe_float("abc") == 0.0
        assert safe_float("123.45", default=999.0) == 123.45
        assert safe_float("", default=999.0) == 999.0
