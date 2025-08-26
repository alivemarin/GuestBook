# Dockerfile

# --- 1단계: 빌드 환경 ---
# 빌드에 필요한 모든 도구를 포함하는 공식 이미지를 사용합니다.
FROM python:3.11-slim-bookworm as builder
# 작업 디렉토리를 설정합니다.
WORKDIR /app
# 취약이 있는 setuptools 버전을 최신으로 업그레이드합니다.
RUN pip install --upgrade pip wheel setuptools
# 의존성 파일을 먼저 복사하여 Docker 레이어 캐싱을 활용합니다.
COPY requirements.txt .
# --prefix /install : 시스템 전체가 아닌 특정 폴더에 라이브러리를 설치합니다.
RUN pip install --prefix=/install -r requirements.txt

# 소스 코드를 복사합니다.
COPY . .

# --- 2단계: 최종 실행 환경 ---
# 훨씬 가볍고 보안 패치가 적용된 최신 slim 이미지를 사용합니다.
FROM python:3.11-slim-bookworm

# 보안 강화를 위해 root가 아닌 일반 사용자를 생성하고 사용합니다.
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# 빌드 환경에서 설치한 라이브러리와 소스 코드만 복사합니다.
COPY --from=builder /install /usr/local
COPY --from=builder /app .

# 애플리케이션 실행
CMD ["python", "app.py"]
