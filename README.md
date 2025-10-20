# 로또 당첨번호 스크래핑 시스템

동행복권 웹사이트에서 로또 1회차부터 최신 회차까지의 모든 당첨번호를 자동으로 수집하여 CSV 파일로 저장하는 Python 스크래핑 도구입니다.

## 🎯 주요 기능

- **자동 데이터 수집**: 로또 1회차부터 최신 회차까지 모든 당첨번호 수집
- **CSV 저장**: 구조화된 데이터를 CSV 형태로 저장
- **에러 처리**: 네트워크 오류 및 웹사이트 구조 변경 대응
- **진행 상황 표시**: 실시간 스크래핑 진행 상황 모니터링

## 📋 요구사항

- Python 3.13+
- Poetry (의존성 관리)
- 인터넷 연결

## 🚀 설치 및 실행

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd scalping_lotto_numbers
```

### 2. 의존성 설치
```bash
# Poetry 설치 (미설치 시)
curl -sSL https://install.python-poetry.org | python3 -

# 의존성 설치
poetry install
```

### 3. 가상환경 활성화
```bash
poetry shell
```

### 4. 스크래핑 실행
```bash
python src/lotto_scraper.py
```

## 📁 프로젝트 구조

```
scalping_lotto_numbers/
├── README.md                 # 프로젝트 설명서
├── PRD.md                    # 제품 요구사항 정의서
├── pyproject.toml           # Poetry 설정 파일
├── poetry.lock              # 의존성 잠금 파일
├── src/                     # 소스 코드
│   ├── __init__.py
│   ├── lotto_scraper.py     # 메인 스크래핑 모듈
│   ├── data_processor.py    # 데이터 처리 모듈
│   └── utils.py             # 유틸리티 함수
├── data/                    # 데이터 저장 디렉토리
│   └── lotto_numbers.csv    # 생성된 CSV 파일
├── tests/                   # 테스트 코드
│   ├── __init__.py
│   ├── test_scraper.py
│   └── test_processor.py
└── config/                  # 설정 파일
    └── settings.py
```

## 📊 데이터 구조

생성되는 CSV 파일의 구조는 다음과 같습니다:

```csv
회차,추첨일,당첨번호1,당첨번호2,당첨번호3,당첨번호4,당첨번호5,당첨번호6,보너스번호,1등당첨자수,1등당첨금액
1,2002-12-07,10,23,29,33,37,40,16,4,2,067,000,000
2,2002-12-14,9,13,21,25,32,42,5,1,1,000,000,000
...
```

## 🛠️ 사용법

### 기본 실행
```bash
python src/lotto_scraper.py
```

### 특정 회차 범위 지정
```bash
python src/lotto_scraper.py --start 1 --end 100
```

### 출력 파일 지정
```bash
python src/lotto_scraper.py --output data/my_lotto_data.csv
```

### 상세 로그 출력
```bash
python src/lotto_scraper.py --verbose
```

## ⚙️ 설정 옵션

`config/settings.py` 파일에서 다음 설정을 조정할 수 있습니다:

- `REQUEST_DELAY`: 요청 간격 (초)
- `MAX_RETRIES`: 최대 재시도 횟수
- `TIMEOUT`: 요청 타임아웃 (초)
- `USER_AGENT`: 사용자 에이전트 문자열

## 🧪 테스트

```bash
# 모든 테스트 실행
poetry run pytest

# 특정 테스트 실행
poetry run pytest tests/test_scraper.py

# 커버리지 포함 테스트
poetry run pytest --cov=src
```

## 📈 성능

- **스크래핑 속도**: 회차당 평균 1초 이내
- **메모리 사용량**: 100MB 이하
- **안정성**: 99% 이상 성공률

## ⚠️ 주의사항

1. **이용약관 준수**: 동행복권 웹사이트의 이용약관을 준수하여 사용하세요.
2. **적절한 요청 간격**: 서버에 과부하를 주지 않도록 적절한 간격으로 요청합니다.
3. **개인정보 보호**: 개인정보를 수집하지 않습니다.

## 🐛 문제 해결

### 일반적인 문제

1. **네트워크 연결 오류**
   ```bash
   # 인터넷 연결 확인
   ping dhlottery.co.kr
   ```

2. **의존성 설치 오류**
   ```bash
   # Poetry 캐시 클리어
   poetry cache clear --all pypi
   poetry install
   ```

3. **권한 오류**
   ```bash
   # 데이터 디렉토리 권한 확인
   chmod 755 data/
   ```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

문제가 발생하거나 질문이 있으시면 다음 방법으로 연락해주세요:

- 이슈 등록: GitHub Issues
- 이메일: puslip41@gmail.com

## 🔄 업데이트 로그

### v1.0.0 (2024-12-19)
- 초기 버전 릴리스
- 기본 스크래핑 기능 구현
- CSV 저장 기능 추가
- 에러 처리 및 로깅 구현

---

**개발자**: puslip41@gmail.com  
**최종 업데이트**: 2024년 12월 19일
