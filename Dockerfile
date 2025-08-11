FROM python:3.10-slim     
#3.11추천해줬는데 우리는 3.10 사용
WORKDIR /app    
#작업디렉토리 형성
COPY requirements.txt .     
#requirements.txt 파일 복사
RUN pip install --no-cache-dir -r requirements.txt
#requirements.txt에 있는 패키지 설치
COPY . .
#현재 디렉토리의 모든 파일을 컨테이너의 /app 디렉토리에 복사
EXPOSE 5000
#컨테이너의 5000번 포트 개방
CMD ["python", "app.py"]
#컨테이너 시작 시 app.py 실행
