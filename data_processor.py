"""
로또 데이터 처리 및 CSV 저장 클래스
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional
import logging

from models import LottoData
from utils import create_output_directory, format_amount
from exceptions import FileOperationError, DataValidationError
from config.settings import PATHS, CSV_CONFIG


class DataProcessor:
    """로또 데이터 처리 및 저장 클래스"""
    
    def __init__(self, output_path: Optional[str] = None):
        """
        데이터 프로세서 초기화
        
        Args:
            output_path: 출력 파일 경로
        """
        self.output_path = Path(output_path) if output_path else PATHS['OUTPUT_FILE']
        self.logger = logging.getLogger('lotto_scraper')
        
        # 출력 디렉토리 생성
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def process_data(self, data: List[LottoData]) -> pd.DataFrame:
        """
        로또 데이터를 DataFrame으로 변환
        
        Args:
            data: LottoData 객체 리스트
            
        Returns:
            pandas DataFrame
        """
        try:
            self.logger.info(f"{len(data)}개 회차 데이터 처리 시작...")
            
            if not data:
                self.logger.warning("처리할 데이터가 없습니다.")
                return pd.DataFrame()
            
            # 데이터를 딕셔너리 리스트로 변환
            data_dicts = [lotto_data.to_dict() for lotto_data in data]
            
            # DataFrame 생성
            df = pd.DataFrame(data_dicts)
            
            # 데이터 검증
            self._validate_dataframe(df)
            
            # 데이터 정렬 (회차순)
            df = df.sort_values('회차').reset_index(drop=True)
            
            self.logger.info(f"데이터 처리 완료: {len(df)}개 행")
            return df
            
        except Exception as e:
            self.logger.error(f"데이터 처리 실패: {e}")
            raise DataValidationError(f"데이터 처리 실패: {e}")
    
    def save_to_csv(self, df: pd.DataFrame, output_path: Optional[str] = None) -> Path:
        """
        DataFrame을 CSV 파일로 저장
        
        Args:
            df: 저장할 DataFrame
            output_path: 출력 파일 경로 (선택사항)
            
        Returns:
            저장된 파일 경로
        """
        try:
            if output_path:
                file_path = Path(output_path)
            else:
                file_path = self.output_path
            
            # 디렉토리 생성
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # CSV 저장
            df.to_csv(
                file_path,
                encoding=CSV_CONFIG['ENCODING'],
                index=CSV_CONFIG['INDEX']
            )
            
            self.logger.info(f"CSV 파일 저장 완료: {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"CSV 저장 실패: {e}")
            raise FileOperationError(f"CSV 저장 실패: {e}")
    
    def load_from_csv(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        CSV 파일에서 데이터 로드
        
        Args:
            file_path: 로드할 파일 경로
            
        Returns:
            pandas DataFrame
        """
        try:
            if file_path:
                path = Path(file_path)
            else:
                path = self.output_path
            
            if not path.exists():
                self.logger.warning(f"파일이 존재하지 않습니다: {path}")
                return pd.DataFrame()
            
            # CSV 로드
            df = pd.read_csv(path, encoding=CSV_CONFIG['ENCODING'])
            
            self.logger.info(f"CSV 파일 로드 완료: {len(df)}개 행")
            return df
            
        except Exception as e:
            self.logger.error(f"CSV 로드 실패: {e}")
            raise FileOperationError(f"CSV 로드 실패: {e}")
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        데이터 유효성 검사
        
        Args:
            df: 검사할 DataFrame
            
        Returns:
            유효성 검사 결과
        """
        try:
            if df.empty:
                self.logger.warning("데이터가 비어있습니다.")
                return False
            
            # 필수 컬럼 확인
            required_columns = CSV_CONFIG['COLUMNS']
            missing_columns = set(required_columns) - set(df.columns)
            if missing_columns:
                self.logger.error(f"필수 컬럼 누락: {missing_columns}")
                return False
            
            # 회차 중복 확인
            if df['회차'].duplicated().any():
                self.logger.error("회차 중복 발견")
                return False
            
            # 당첨번호 유효성 검사
            for i in range(1, 7):
                col_name = f'당첨번호{i}'
                if col_name in df.columns:
                    invalid_numbers = df[~df[col_name].between(1, 45)]
                    if not invalid_numbers.empty:
                        self.logger.error(f"{col_name}에 유효하지 않은 번호 발견")
                        return False
            
            # 보너스번호 유효성 검사
            if '보너스번호' in df.columns:
                invalid_bonus = df[~df['보너스번호'].between(1, 45)]
                if not invalid_bonus.empty:
                    self.logger.error("보너스번호에 유효하지 않은 번호 발견")
                    return False
            
            self.logger.info("데이터 유효성 검사 통과")
            return True
            
        except Exception as e:
            self.logger.error(f"데이터 유효성 검사 실패: {e}")
            return False
    
    def _validate_dataframe(self, df: pd.DataFrame):
        """DataFrame 내부 검증"""
        if df.empty:
            raise DataValidationError("DataFrame이 비어있습니다.")
        
        # 회차 컬럼 확인
        if '회차' not in df.columns:
            raise DataValidationError("회차 컬럼이 없습니다.")
        
        # 회차 중복 확인
        if df['회차'].duplicated().any():
            raise DataValidationError("회차에 중복이 있습니다.")
    
    def get_statistics(self, df: pd.DataFrame) -> dict:
        """
        데이터 통계 정보 생성
        
        Args:
            df: 통계를 생성할 DataFrame
            
        Returns:
            통계 정보 딕셔너리
        """
        try:
            if df.empty:
                return {}
            
            stats = {
                '총_회차수': len(df),
                '시작_회차': df['회차'].min(),
                '종료_회차': df['회차'].max(),
                '시작_날짜': df['추첨일'].min(),
                '종료_날짜': df['추첨일'].max(),
                '평균_1등당첨자수': df['1등당첨자수'].mean(),
                '평균_1등당첨금액': df['1등당첨금액'].mean(),
                '최대_1등당첨금액': df['1등당첨금액'].max(),
                '최소_1등당첨금액': df['1등당첨금액'].min()
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"통계 생성 실패: {e}")
            return {}
    
    def print_statistics(self, df: pd.DataFrame):
        """통계 정보 출력"""
        stats = self.get_statistics(df)
        
        if not stats:
            self.logger.warning("통계 정보를 생성할 수 없습니다.")
            return
        
        print("\n" + "="*50)
        print("📊 로또 데이터 통계")
        print("="*50)
        print(f"총 회차수: {stats['총_회차수']:,}회")
        print(f"회차 범위: {stats['시작_회차']}회 ~ {stats['종료_회차']}회")
        print(f"날짜 범위: {stats['시작_날짜']} ~ {stats['종료_날짜']}")
        print(f"평균 1등 당첨자수: {stats['평균_1등당첨자수']:.1f}명")
        print(f"평균 1등 당첨금액: {format_amount(int(stats['평균_1등당첨금액']))}원")
        print(f"최대 1등 당첨금액: {format_amount(int(stats['최대_1등당첨금액']))}원")
        print(f"최소 1등 당첨금액: {format_amount(int(stats['최소_1등당첨금액']))}원")
        print("="*50)
