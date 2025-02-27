# 🐳 기본 이미지: Python 3.9 + 최신 MLflow 지원
FROM python:3.9-slim

# 🏗️ 작업 디렉토리 설정
WORKDIR /

# 📝 종속성 설치 (FastAPI, MLflow 등)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 📜 FastAPI 코드 복사
COPY app.py .

# 🚀 FastAPI 서버 실행 (Uvicorn 사용)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
