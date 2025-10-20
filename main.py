"""
로또 당첨번호 스크래핑 메인 실행 파일
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from lotto_scraper import LottoScraper
from data_processor import DataProcessor
from utils import setup_logging
from exceptions import LottoScrapingError


def parse_arguments():
    """명령행 인수 파싱"""
    parser = argparse.ArgumentParser(
        description='로또 당첨번호 스크래핑 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python main.py                           # 전체 회차 스크래핑
  python main.py --start 1 --end 100       # 1회차부터 100회차까지
  python main.py --output data/my_data.csv  # 출력 파일 지정
  python main.py --verbose                  # 상세 로그 출력
        """
    )
    
    parser.add_argument(
        '--start',
        type=int,
        default=1,
        help='시작 회차 (기본값: 1)'
    )
    
    parser.add_argument(
        '--end',
        type=int,
        help='종료 회차 (기본값: 최신 회차)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='출력 CSV 파일 경로 (기본값: data/lotto_numbers.csv)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='상세 로그 출력'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='요청 간격 (초) (기본값: 1.0)'
    )
    
    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='최대 재시도 횟수 (기본값: 3)'
    )
    
    return parser.parse_args()


def main():
    """메인 실행 함수"""
    try:
        # 명령행 인수 파싱
        args = parse_arguments()
        
        # 로깅 설정
        log_level = 'DEBUG' if args.verbose else 'INFO'
        logger = setup_logging(log_level)
        
        logger.info("로또 스크래핑 시작")
        logger.info(f"시작 회차: {args.start}")
        logger.info(f"종료 회차: {args.end if args.end else '최신 회차'}")
        logger.info(f"출력 파일: {args.output if args.output else 'data/lotto_numbers.csv'}")
        
        # 스크래퍼 초기화
        scraper = LottoScraper()
        
        # 데이터 프로세서 초기화
        processor = DataProcessor(args.output)
        
        try:
            # 스크래핑 실행
            logger.info("스크래핑 시작...")
            lotto_data = scraper.scrape_all_rounds(args.start, args.end)
            
            if not lotto_data:
                logger.error("스크래핑된 데이터가 없습니다.")
                sys.exit(1)
            
            # 데이터 처리
            logger.info("데이터 처리 중...")
            df = processor.process_data(lotto_data)
            
            # 데이터 검증
            if not processor.validate_data(df):
                logger.error("데이터 검증 실패")
                sys.exit(1)
            
            # CSV 저장
            logger.info("CSV 파일 저장 중...")
            output_path = processor.save_to_csv(df)
            
            # 통계 출력
            processor.print_statistics(df)
            
            logger.info(f"스크래핑 완료: {output_path}")
            print(f"\n✅ 스크래핑이 성공적으로 완료되었습니다!")
            print(f"📁 저장된 파일: {output_path}")
            print(f"📊 총 {len(df)}개 회차 데이터")
            
        finally:
            # 리소스 정리
            scraper.close()
            
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
        
    except LottoScrapingError as e:
        print(f"\n❌ 스크래핑 오류: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n💥 예상치 못한 오류: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
