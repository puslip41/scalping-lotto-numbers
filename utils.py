"""
로또 스크래핑 유틸리티 함수들
"""

import re
import time
import logging
from typing import List, Optional
from pathlib import Path
from config.settings import PATHS, LOGGING_CONFIG


def setup_logging(log_level: str = 'INFO') -> logging.Logger:
    """로깅 설정"""
    # 로그 디렉토리 생성
    PATHS['LOGS_DIR'].mkdir(exist_ok=True)
    
    # 로거 설정
    logger = logging.getLogger('lotto_scraper')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 핸들러가 이미 있으면 제거
    if logger.handlers:
        logger.handlers.clear()
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # 파일 핸들러
    log_file = PATHS['LOGS_DIR'] / 'lotto_scraper.log'
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # 포매터
    formatter = logging.Formatter(LOGGING_CONFIG['FORMAT'])
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 핸들러 추가
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def clean_number_string(text: str) -> int:
    """숫자 문자열을 정수로 변환 (콤마 제거)"""
    if not text:
        return 0
    
    # 숫자가 아닌 문자 제거
    cleaned = re.sub(r'[^\d]', '', text)
    return int(cleaned) if cleaned else 0


def parse_date_string(date_str: str) -> str:
    """날짜 문자열을 YYYY-MM-DD 형식으로 변환"""
    if not date_str:
        return ""
    
    # 다양한 날짜 형식 처리
    date_patterns = [
        r'(\d{4})\.(\d{1,2})\.(\d{1,2})',  # 2024.12.19
        r'(\d{4})-(\d{1,2})-(\d{1,2})',   # 2024-12-19
        r'(\d{4})/(\d{1,2})/(\d{1,2})',   # 2024/12/19
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, date_str)
        if match:
            year, month, day = match.groups()
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    return date_str


def validate_winning_numbers(numbers: List[int]) -> bool:
    """당첨번호 유효성 검사"""
    if len(numbers) != 6:
        return False
    
    # 범위 검사
    for num in numbers:
        if not (1 <= num <= 45):
            return False
    
    # 중복 검사
    if len(set(numbers)) != len(numbers):
        return False
    
    return True


def validate_bonus_number(bonus: int, winning_numbers: List[int]) -> bool:
    """보너스번호 유효성 검사"""
    # 범위 검사
    if not (1 <= bonus <= 45):
        return False
    
    # 당첨번호와 중복 검사
    if bonus in winning_numbers:
        return False
    
    return True


def create_output_directory() -> Path:
    """출력 디렉토리 생성"""
    output_dir = PATHS['DATA_DIR']
    output_dir.mkdir(exist_ok=True)
    return output_dir


def format_amount(amount: int) -> str:
    """금액을 천단위 콤마 형식으로 변환"""
    return f"{amount:,}"


def safe_int(value: str, default: int = 0) -> int:
    """안전한 정수 변환"""
    try:
        if not value:
            return default
        # 소수점이 있는 경우 정수 부분만 추출
        if '.' in str(value):
            return int(float(value))
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: str, default: float = 0.0) -> float:
    """안전한 실수 변환"""
    try:
        return float(value) if value else default
    except (ValueError, TypeError):
        return default


def retry_on_exception(max_retries: int = 3, delay: float = 1.0):
    """예외 발생 시 재시도 데코레이터"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # 지수 백오프
                        continue
                    else:
                        raise last_exception
            
            return None
        return wrapper
    return decorator
