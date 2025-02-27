FROM python:3.9-slim

WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 모델 학습 스크립트 복사
COPY regression_example.py .

# 스크립트 실행
CMD ["python", "regression_example.py"]