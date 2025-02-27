#!/bin/bash
CONTAINER_NAME="mlflow-api"

if docker ps -q -f name=$CONTAINER_NAME; then
    echo "🛑 실행 중인 '$CONTAINER_NAME' 컨테이너 중지 중..."
    docker stop $CONTAINER_NAME
    echo "✅ 컨테이너 중지 완료!"
fi

if docker ps -aq -f name=$CONTAINER_NAME; then
    echo "🗑️  기존 '$CONTAINER_NAME' 컨테이너 삭제 중..."
    docker rm $CONTAINER_NAME
    echo "✅ 컨테이너 삭제 완료!"
fi

echo "🚀 '$CONTAINER_NAME' 컨테이너 실행 중..."
docker run --network mlflow-network -p 8000:8000 --name $CONTAINER_NAME fastapi-mlflow-server
echo "✅ 컨테이너 실행 완료!"
