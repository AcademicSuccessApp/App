import joblib
import pandas as pd

# Load model and encoders (no scaler)
model = joblib.load('public/models/best_model_v1.pkl')
le_program_studi = joblib.load('public/models/le_program_studi_v1.pkl')
le_dosen = joblib.load('public/models/le_dosen_v1.pkl')

# Example input (change these values to test different scenarios)
data = {
    'Sem 1': 4.0,
    'Sem 2': 4.0,
    'Sem 3': 4.0,
    'rata2_IPS': (4.0 + 4.0 + 4.0) / 3,
    'program_studi': 'S1 Teknik Informatika - Kampus Purwokerto',
    'kode_dosen': 'ANT'
}

# Convert to DataFrame
df = pd.DataFrame([data])

# Encode categorical features
df['program_studi_le'] = le_program_studi.transform(df['program_studi'].astype(str))
df['kode_dosen_le'] = le_dosen.transform(df['kode_dosen'].astype(str))

# Select features (no scaling)
feature_cols = ['Sem 1', 'Sem 2', 'Sem 3', 'rata2_IPS', 'program_studi_le', 'kode_dosen_le']
X = df[feature_cols]

# Predict
prediction = model.predict(X)[0]
print("Prediction (1=Likely to Graduate on Time, 0=At Risk to Graduate Late):", prediction)

# If you want to see the probability (optional, for debugging)
if hasattr(model, "predict_proba"):
    proba = model.predict_proba(X)[0]
    print("Probabilities:", proba)