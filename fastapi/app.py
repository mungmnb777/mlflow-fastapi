import mlflow
import mlflow.pyfunc
from mlflow.tracking import MlflowClient
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

# FastAPI 앱 초기화
app = FastAPI()

# MLflow 설정
mlflow.set_tracking_uri("http://mlflow-server:5000")
model_name = "study_hours_regressor"

# ✅ 최신 모델 버전 가져오기
client = MlflowClient()
latest_version = max([
    int(m.version) for m in client.search_model_versions(f"name='{model_name}'")
])

# ✅ 최신 모델 로드
model_uri = f"models:/{model_name}/{latest_version}"
model = mlflow.pyfunc.load_model(model_uri)


# 📌 요청 데이터 형식 정의
class StudyHoursInput(BaseModel):
    study_hours: float

@app.get("/")
def root():
    return {"message": "MLflow Model API is running!"}

# ✅ 예측 API 엔드포인트
@app.post("/predict")
def predict(input_data: StudyHoursInput):
    try:
        # 입력 데이터 처리
        X_input = np.array([[input_data.study_hours]])
        
        # 예측 수행
        prediction = model.predict(X_input)
        
        return {
            "study_hours": input_data.study_hours,
            "predicted_test_score": float(prediction[0])
        }
    
    except Exception as e:
        return {"error": str(e)}

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
