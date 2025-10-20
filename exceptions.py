"""
로또 스크래핑 관련 커스텀 예외 클래스들
"""


class LottoScrapingError(Exception):
    """로또 스크래핑 기본 예외 클래스"""
    pass


class NetworkError(LottoScrapingError):
    """네트워크 관련 오류"""
    pass


class ParsingError(LottoScrapingError):
    """HTML 파싱 관련 오류"""
    pass


class DataValidationError(LottoScrapingError):
    """데이터 검증 관련 오류"""
    pass


class FileOperationError(LottoScrapingError):
    """파일 작업 관련 오류"""
    pass
