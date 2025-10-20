"""
로또 당첨번호 스크래핑 메인 클래스
"""

import time
import re
import requests
from bs4 import BeautifulSoup
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin
import logging

from models import LottoData
from utils import (
    setup_logging, clean_number_string, parse_date_string,
    validate_winning_numbers, validate_bonus_number, retry_on_exception
)
from exceptions import NetworkError, ParsingError, DataValidationError
from config.settings import SCRAPING_CONFIG


class LottoScraper:
    """로또 당첨번호 스크래핑 클래스"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        스크래퍼 초기화
        
        Args:
            config: 스크래핑 설정 딕셔너리
        """
        self.config = config or SCRAPING_CONFIG
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.config['USER_AGENT']
        })
        self.logger = setup_logging()
        
    def get_latest_round(self) -> int:
        """최신 회차 번호 조회"""
        try:
            self.logger.info("최신 회차 조회 중...")
            
            # 메인 페이지에서 최신 회차 정보 추출
            # BASE_URL 단독 호출 시 400 응답이 발생하므로 method 파라미터를 포함해 요청한다
            response = self._make_request(f"{self.config['BASE_URL']}?method=byWin")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 최신 회차 번호 추출 로직
            latest_round = self._extract_latest_round(soup)
            
            self.logger.info(f"최신 회차: {latest_round}")
            return latest_round
            
        except Exception as e:
            self.logger.error(f"최신 회차 조회 실패: {e}")
            raise NetworkError(f"최신 회차 조회 실패: {e}")
    
    def scrape_round(self, round_num: int) -> Optional[LottoData]:
        """
        특정 회차 데이터 스크래핑
        
        Args:
            round_num: 회차 번호
            
        Returns:
            LottoData 객체 또는 None
        """
        try:
            self.logger.info(f"회차 {round_num} 스크래핑 시작...")
            
            # 요청 URL 구성
            url = f"{self.config['BASE_URL']}?method=byWin&drwNo={round_num}"
            
            # HTTP 요청
            response = self._make_request(url)
            
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 데이터 추출
            lotto_data = self._parse_round_data(soup, round_num)
            
            if lotto_data:
                self.logger.info(f"회차 {round_num} 스크래핑 완료")
            else:
                self.logger.warning(f"회차 {round_num} 데이터 없음")
            
            # 요청 간격 대기
            time.sleep(self.config['REQUEST_DELAY'])
            
            return lotto_data
            
        except Exception as e:
            self.logger.error(f"회차 {round_num} 스크래핑 실패: {e}")
            return None
    
    def scrape_all_rounds(self, start: int = 1, end: Optional[int] = None) -> List[LottoData]:
        """
        전체 회차 데이터 스크래핑
        
        Args:
            start: 시작 회차
            end: 종료 회차 (None이면 최신 회차까지)
            
        Returns:
            LottoData 객체 리스트
        """
        if end is None:
            end = self.get_latest_round()
        
        self.logger.info(f"회차 {start}부터 {end}까지 스크래핑 시작...")
        
        results = []
        failed_rounds = []
        
        for round_num in range(start, end + 1):
            try:
                lotto_data = self.scrape_round(round_num)
                if lotto_data:
                    results.append(lotto_data)
                else:
                    failed_rounds.append(round_num)
                    
            except Exception as e:
                self.logger.error(f"회차 {round_num} 처리 중 오류: {e}")
                failed_rounds.append(round_num)
        
        self.logger.info(f"스크래핑 완료: 성공 {len(results)}개, 실패 {len(failed_rounds)}개")
        
        if failed_rounds:
            self.logger.warning(f"실패한 회차: {failed_rounds}")
        
        return results
    
    @retry_on_exception(max_retries=3, delay=1.0)
    def _make_request(self, url: str) -> requests.Response:
        """HTTP 요청 (재시도 로직 포함)"""
        try:
            response = self.session.get(
                url, 
                timeout=self.config['TIMEOUT']
            )
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"HTTP 요청 실패: {e}")
    
    def _extract_latest_round(self, soup: BeautifulSoup) -> int:
        """최신 회차 번호 추출"""
        try:
            # 회차 선택 드롭다운에서 최신 회차 추출
            select_element = soup.find('select', {'id': 'dwrNoList'})
            if select_element:
                options = select_element.find_all('option')
                if options:
                    # 첫 번째 옵션이 최신 회차
                    latest_round = int(options[0].get('value', 0))
                    return latest_round
            
            # 대안: 메타 태그에서 회차 정보 추출
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                content = meta_desc.get('content')
                match = re.search(r'(\d+)회', content)
                if match:
                    return int(match.group(1))
            
            # 기본값 반환 (현재 시점 기준 대략적인 최신 회차)
            return 1200  # 2024년 기준 대략적인 회차
            
        except Exception as e:
            self.logger.warning(f"최신 회차 추출 실패, 기본값 사용: {e}")
            return 1200
    
    def _parse_round_data(self, soup: BeautifulSoup, round_num: int) -> Optional[LottoData]:
        """회차 데이터 파싱"""
        try:
            # 당첨번호 추출
            winning_numbers = self._extract_winning_numbers(soup)
            if not winning_numbers:
                return None
            
            # 보너스번호 추출
            bonus_number = self._extract_bonus_number(soup)
            if not bonus_number:
                return None
            
            # 추첨일 추출
            draw_date = self._extract_draw_date(soup)
            if not draw_date:
                return None
            
            # 당첨자수 및 당첨금액 추출
            first_prize_winners, first_prize_amount = self._extract_prize_info(soup)
            
            # 데이터 검증
            if not validate_winning_numbers(winning_numbers):
                raise DataValidationError(f"회차 {round_num}: 당첨번호 검증 실패")
            
            if not validate_bonus_number(bonus_number, winning_numbers):
                raise DataValidationError(f"회차 {round_num}: 보너스번호 검증 실패")
            
            return LottoData(
                round_num=round_num,
                draw_date=draw_date,
                winning_numbers=winning_numbers,
                bonus_number=bonus_number,
                first_prize_winners=first_prize_winners,
                first_prize_amount=first_prize_amount
            )
            
        except Exception as e:
            self.logger.error(f"회차 {round_num} 데이터 파싱 실패: {e}")
            raise ParsingError(f"회차 {round_num} 데이터 파싱 실패: {e}")
    
    def _extract_winning_numbers(self, soup: BeautifulSoup) -> List[int]:
        """당첨번호 추출"""
        try:
            # 당첨번호가 있는 요소 찾기 (당첨번호 섹션)
            winning_section = soup.find('div', class_='num win')
            if not winning_section:
                self.logger.warning("당첨번호 섹션을 찾을 수 없습니다")
                return []
            
            # 당첨번호 공들 추출
            ball_elements = winning_section.find_all('span', class_='ball_645')
            
            if not ball_elements:
                self.logger.warning("당첨번호 공을 찾을 수 없습니다")
                return []
            
            numbers = []
            for element in ball_elements:
                num = clean_number_string(element.text)
                if 1 <= num <= 45:
                    numbers.append(num)
            
            # 6개 번호인지 확인
            if len(numbers) == 6:
                return numbers
            else:
                self.logger.warning(f"당첨번호 개수가 올바르지 않습니다: {len(numbers)}개")
                return []
            
        except Exception as e:
            self.logger.error(f"당첨번호 추출 실패: {e}")
            return []
    
    def _extract_bonus_number(self, soup: BeautifulSoup) -> Optional[int]:
        """보너스번호 추출"""
        try:
            # 보너스번호가 있는 요소 찾기 (보너스 섹션)
            bonus_section = soup.find('div', class_='num bonus')
            if not bonus_section:
                self.logger.warning("보너스번호 섹션을 찾을 수 없습니다")
                return None
            
            # 보너스번호 공 추출
            bonus_element = bonus_section.find('span', class_='ball_645')
            if not bonus_element:
                self.logger.warning("보너스번호 공을 찾을 수 없습니다")
                return None
            
            bonus_number = clean_number_string(bonus_element.text)
            if 1 <= bonus_number <= 45:
                return bonus_number
            else:
                self.logger.warning(f"보너스번호가 올바르지 않습니다: {bonus_number}")
                return None
            
        except Exception as e:
            self.logger.error(f"보너스번호 추출 실패: {e}")
            return None
    
    def _extract_draw_date(self, soup: BeautifulSoup) -> Optional[str]:
        """추첨일 추출"""
        try:
            # 메타 태그에서 날짜 정보 추출
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                content = meta_desc.get('content')
                # 날짜 패턴 찾기 (예: 2025.03.14)
                date_match = re.search(r'(\d{4}\.\d{1,2}\.\d{1,2})', content)
                if date_match:
                    date_str = date_match.group(1)
                    return parse_date_string(date_str)
            
            # 대안: 페이지에서 날짜 패턴 직접 검색
            date_elements = soup.find_all(text=re.compile(r'\d{4}[-./]\d{1,2}[-./]\d{1,2}'))
            if date_elements:
                date_str = date_elements[0].strip()
                return parse_date_string(date_str)
            
            return None
            
        except Exception as e:
            self.logger.error(f"추첨일 추출 실패: {e}")
            return None
    
    def _extract_prize_info(self, soup: BeautifulSoup) -> tuple[int, int]:
        """당첨자수 및 당첨금액 추출"""
        try:
            # 1등 당첨자수와 당첨금액을 테이블에서 추출
            table = soup.find('table', class_='tbl_data')
            if not table:
                self.logger.warning("당첨정보 테이블을 찾을 수 없습니다")
                return 0, 0
            
            # 1등 행 찾기
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 4 and cells[0].text.strip() == '1등':
                    # 당첨자수 (3번째 셀)
                    winners_text = cells[2].text.strip()
                    winners = clean_number_string(winners_text)
                    
                    # 1게임당 당첨금액 (4번째 셀)
                    amount_text = cells[3].text.strip()
                    amount = clean_number_string(amount_text)
                    
                    return winners, amount
            
            # 대안: 메타 태그에서 정보 추출
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                content = meta_desc.get('content')
                # 1등 총 28명, 1인당 당첨금액 985,155,349원 패턴
                match = re.search(r'1등 총 (\d+)명.*?(\d{1,3}(?:,\d{3})*)원', content)
                if match:
                    winners = clean_number_string(match.group(1))
                    amount = clean_number_string(match.group(2))
                    return winners, amount
            
            return 0, 0
            
        except Exception as e:
            self.logger.error(f"당첨정보 추출 실패: {e}")
            return 0, 0
    
    def close(self):
        """세션 종료"""
        if hasattr(self, 'session'):
            self.session.close()
