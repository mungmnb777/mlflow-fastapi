#!/bin/bash

MLFLOW_URL=${1:-"http://localhost:5000"}
HEALTH_ENDPOINT="${MLFLOW_URL}/health"

echo "🏥 MLflow 서버 헬스 체크 실행 중..."
echo "💻 확인 URL: ${HEALTH_ENDPOINT}"

# 헬스 체크 요청
response=$(curl -s -o /dev/null -w "%{http_code}" ${HEALTH_ENDPOINT})

if [ "$response" = "200" ]; then
  echo "✅ MLflow 서버가 정상적으로 작동 중입니다. (상태 코드: ${response})"
  
  # MLflow 서버의 상세 정보 가져오기
  echo "📊 MLflow 서버 상세 정보:"
  
  # 등록된 모델 목록 확인
  echo "🔍 등록된 모델 목록 확인 중..."
  models_response=$(curl -s "${MLFLOW_URL}/api/2.0/mlflow/registered-models/list")
  registered_models=$(echo $models_response | grep -o '"registered_models":\[.*\]' || echo "등록된 모델이 없습니다.")
  
  if [ "$registered_models" != "등록된 모델이 없습니다." ]; then
    echo "📋 등록된 모델 목록:"
    echo $models_response | grep -o '"name":"[^"]*"' | cut -d'"' -f4
  else
    echo "⚠️ 등록된 모델이 없습니다."
  fi
  
  # 실험 목록 확인
  echo "🧪 실험 목록 확인 중..."
  experiments_response=$(curl -s "${MLFLOW_URL}/api/2.0/mlflow/experiments/list")
  echo "📋 실험 목록:"
  echo $experiments_response | grep -o '"name":"[^"]*"' | cut -d'"' -f4
  
  exit 0
else
  echo "❌ MLflow 서버에 연결할 수 없거나 서버가 비정상입니다. (상태 코드: ${response})"
  
  # 컨테이너 상태 확인
  echo "🔍 Docker 컨테이너 상태 확인:"
  docker ps -a | grep mlflow-server
  
  # 로그 확인
  echo "📜 MLflow 서버 로그 (최근 10줄):"
  docker logs --tail 10 mlflow-server
  
  exit 1
fi