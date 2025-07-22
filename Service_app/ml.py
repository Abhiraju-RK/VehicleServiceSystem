import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

MODEL_PATH=os.path.join('Service_app','ml_model.pkl')

def train_model(csv_path):
    df=pd.read_csv(csv_path)
    X = df[['vehicle_age', 'last_service_days', 'km_run']]
    y = df['next_breakdown_risk']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model trained with accuracy: {acc:.2f}")

    joblib.dump(model, MODEL_PATH)

def predict_maintenance(vehicle_age, last_service_days, km_run):
    if not os.path.exists(MODEL_PATH):
        raise Exception("Model not trained yet. Please run train_model() first.")

    model = joblib.load(MODEL_PATH)
    prediction = model.predict([[vehicle_age, last_service_days, km_run]])
    return int(prediction[0])