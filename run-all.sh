#!/bin/bash

# Docker 네트워크 생성 (이미 있으면 무시)
echo "🌐 Docker 네트워크 설정 중..."
docker network create mlflow-network 2>/dev/null || true

# Docker Compose를 사용하여 전체 시스템 시작
echo "🚀 MLflow + FastAPI 시스템 시작 중..."
docker-compose up -d

# 로그 보기
echo "📋 로그를 확인하려면 다음 명령어를 실행하세요:"
echo "docker-compose logs -f"

# 접속 정보 출력
echo "🔗 서비스 접속 정보:"
echo "- MLflow 서버: http://localhost:5000"
echo "- FastAPI 서버: http://localhost:8000"
echo "- FastAPI 문서: http://localhost:8000/docs"