# Dockerfile

# --- 1단계: 빌드 환경 ---
# 빌드에 필요한 모든 도구를 포함하는 공식 이미지를 사용합니다. (slim 대신 alpine 사용)
FROM python:3.11-alpine as builder
# 작업 디렉토리를 설정합니다.
WORKDIR /app
# 빌드에 필요한 패키지를 설치합니다.
RUN apk add --no-cache build-base
# 의존성 파일을 먼저 복사하여 Docker 레이어 캐싱을 활용합니다.
COPY requirements.txt .

# --target /app/packages : 애플리케이션이 참조할 수 있는 경로에 설치합니다.
RUN pip install --target=/app/packages -r requirements.txt

# 소스 코드를 복사합니다.
COPY . .

# --- 2단계: 최종 실행 환경 ---
# 더 작고 보안성이 강화된 이미지 사용 (Distroless로 대체)
FROM gcr.io/distroless/python3:3.11-nonroot



# 빌드 환경에서 설치한 라이브러리와 소스 코드만 복사합니다.
COPY --from=builder /app/packages /app/packages
COPY --from=builder /app /app

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# 환경 변수 설정
ENV PYTHONPATH=/app/packages

# 애플리케이션 실행
CMD ["python", "app.py"]
