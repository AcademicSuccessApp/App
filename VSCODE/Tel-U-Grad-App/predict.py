import sys
import json
import joblib
import numpy as np
import pandas as pd

def predict(sem1, sem2, sem3, program_studi, kode_dosen):
    try:
        # Load the models
        model = joblib.load('public/models/best_model_v1.pkl')
        le_program_studi = joblib.load('public/models/le_program_studi_v1.pkl')
        le_dosen = joblib.load('public/models/le_dosen_v1.pkl')

        # Create input data
        data = {
            'Sem 1': float(sem1),
            'Sem 2': float(sem2),
            'Sem 3': float(sem3),
            'rata2_IPS': (float(sem1) + float(sem2) + float(sem3)) / 3,
            'program_studi': program_studi,
            'kode_dosen': kode_dosen
        }

        # Convert to DataFrame
        df = pd.DataFrame([data])

        # Apply label encoding
        df['program_studi_le'] = le_program_studi.transform(df['program_studi'].astype(str))
        df['kode_dosen_le'] = le_dosen.transform(df['kode_dosen'].astype(str))

        # Select features (no scaling)
        feature_cols = ['Sem 1', 'Sem 2', 'Sem 3', 'rata2_IPS', 'program_studi_le', 'kode_dosen_le']
        X = df[feature_cols]

        # Make prediction (no scaling)
        prediction = model.predict(X)[0]
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)[0]
            prob_pred = float(proba[prediction])  # Probability for the predicted class
        else:
            prob_pred = None

        # Prepare response
        result = {
            'status': 'Likely to Graduate' if prediction == 1 else 'At Risk',
            'probability': prob_pred,
            'recommendation': get_recommendation(prediction, data)
        }

        print(json.dumps(result))
        return 0

    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

def get_recommendation(prediction, data):
    if prediction == 1:
        return "Good performance! Continue working hard to maintain your grades."
    else:
        if data['rata2_IPS'] < 2.0:
            return "Focus on improving your grades. Consider seeking academic support and managing your study time better."
        elif data['rata2_IPS'] < 2.5:
            return "Your grades need improvement. Consider reviewing your study methods and seeking help from lecturers."
        else:
            return "You're close to the threshold. Focus on maintaining or improving your current performance."

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python predict.py <sem1> <sem2> <sem3> <program_studi> <kode_dosen>", file=sys.stderr)
        sys.exit(1)

    sys.exit(predict(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])) 