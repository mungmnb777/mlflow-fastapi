import os
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import time

# Docker 컨테이너 내에서 MLflow 서버 주소 설정
mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("Improved Time-Series Regression Model")

os.environ["MLFLOW_ARTIFACT_LOCATION"] = "/home/appuser/mlflow"

# 연결 상태 출력
print("📡 MLflow 서버에 연결 중...")

with mlflow.start_run(run_name="register_model"):

    # 데이터 생성
    np.random.seed(42)
    n_samples = 100
    study_hours = np.random.uniform(1, 20, n_samples)
    noise = np.random.normal(0, 10, n_samples)
    test_score = 50 + 3 * study_hours + 0.5 * (study_hours ** 2) + noise

    df = pd.DataFrame({
        "study_hours": study_hours,
        "test_score": test_score
    })

    # 데이터 분리
    X = df[["study_hours"]]
    y = df["test_score"]

    # 데이터 스케일링
    scaler_x = StandardScaler()
    X_scaled = scaler_x.fit_transform(X)

    scaler_y = StandardScaler()
    y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()

    # 모델 학습
    print("🔄 모델 학습 중...")
    model = SGDRegressor(max_iter=1000, tol=1e-3, random_state=42)
    model.fit(X_scaled, y_scaled)

    # 모델 평가
    y_pred_scaled = model.predict(X_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()
    
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    print(f"📊 모델 성능: MSE={mse:.2f}, R²={r2:.2f}")

    # MLflow 로깅
    mlflow.log_param("model_type", "SGDRegressor")
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2_score", r2)
    
    # 모델 저장 및 등록
    model_name = "study_hours_regressor"
    model_info = mlflow.sklearn.log_model(
        model, 
        model_name,
        input_example=X_scaled[:5]  # 입력 데이터 예시 제공
    )

    # ✅ 모델을 MLflow Model Registry에 등록
    print("🚀 모델 등록 중...")
    registered_model = mlflow.register_model(
        model_uri=model_info.model_uri,
        name=model_name
    )

    # ✅ 최신 모델을 "Production" 버전으로 설명 업데이트 (Alias 없이 관리)
    client = MlflowClient()
    client.update_model_version(
        name=model_name,
        version=registered_model.version,
        description="Production-ready model"
    )
    print("✅ MLflow 서버에 성공적으로 연결되었습니다.")

    print(f"✅ 모델 등록 완료: {registered_model.name} - Version {registered_model.version}")
    print(f"📌 모델 설명을 'Production-ready model'로 설정")

mlflow.end_run()

# FastAPI 서비스가 모델을 로드할 시간을 주기 위해 잠시 대기
print("⏳ 모든 작업이 완료되었습니다. 서비스가 안정화될 때까지 잠시 대기합니다...")
time.sleep(10)
print("🏁 완료!")