"""
로또 스크래핑 설정 파일
"""

import os
from pathlib import Path

# 프로젝트 루트 디렉토리
PROJECT_ROOT = Path(__file__).parent.parent

# 스크래핑 설정
SCRAPING_CONFIG = {
    'BASE_URL': 'https://dhlottery.co.kr/gameResult.do',
    'REQUEST_DELAY': 1.0,  # 요청 간격 (초)
    'MAX_RETRIES': 3,      # 최대 재시도 횟수
    'TIMEOUT': 10,         # 요청 타임아웃 (초)
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# 파일 경로 설정
PATHS = {
    'DATA_DIR': PROJECT_ROOT / 'data',
    'LOGS_DIR': PROJECT_ROOT / 'logs',
    'OUTPUT_FILE': PROJECT_ROOT / 'data' / 'lotto_numbers.csv',
}

# 로깅 설정
LOGGING_CONFIG = {
    'LEVEL': 'INFO',
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'LOG_FILE': str(PROJECT_ROOT / 'logs' / 'lotto_scraper.log'),
}

# 데이터 검증 설정
VALIDATION_CONFIG = {
    'MIN_NUMBER': 1,
    'MAX_NUMBER': 45,
    'WINNING_NUMBERS_COUNT': 6,
    'BONUS_NUMBER_COUNT': 1,
}

# CSV 출력 설정
CSV_CONFIG = {
    'ENCODING': 'utf-8',
    'INDEX': False,
    'COLUMNS': [
        '회차', '추첨일', '당첨번호1', '당첨번호2', '당첨번호3', 
        '당첨번호4', '당첨번호5', '당첨번호6', '보너스번호', 
        '1등당첨자수', '1등당첨금액'
    ]
}
