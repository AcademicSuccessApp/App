import sys
import json
import joblib
import numpy as np
import pandas as pd
import traceback

def predict(sem1, sem2, sem3, sem4, gender, program_studi):
    try:
        # Input validation and processing for semesters
        sem_values = []
        processed_semesters = {}
        for i, sem_arg in enumerate([sem1, sem2, sem3, sem4]):
            sem_num = i + 1
            if sem_arg is None or sem_arg == '':
                processed_semesters[f'Sem {sem_num}'] = None # Mark as missing
            else:
                try:
                    sem_float = float(sem_arg)
                    if not (0 <= sem_float <= 4):
                        raise ValueError(f"Semester {sem_num} GPA must be between 0 and 4, got {sem_float}")
                    processed_semesters[f'Sem {sem_num}'] = sem_float
                    sem_values.append(sem_float)
                except ValueError as e:
                    raise ValueError(f"Invalid GPA value for Semester {sem_num}: {sem_arg}") from e

        # Calculate rata2_IPS and impute missing semester values
        if sem_values:
            rata2_IPS = sum(sem_values) / len(sem_values)
        else:
            # Default if no semesters are provided
            rata2_IPS = 3.0

        # Impute missing semesters with calculated rata2_IPS or default if no semesters were provided
        for sem_key in ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']:
            if processed_semesters[sem_key] is None:
                processed_semesters[sem_key] = rata2_IPS

        if gender.lower() not in ['laki-laki', 'perempuan']:
            raise ValueError(f"Invalid gender: {gender}. Must be 'Laki-laki' or 'Perempuan'")

        # Load the models and encoder (no scaler)
        try:
            classification_model = joblib.load('public/models/best_classification_model.pkl')
            regression_model = joblib.load('public/models/best_regression_model.pkl')
            le_program_studi = joblib.load('public/models/le_program_studi_v1.pkl')
        except Exception as e:
            raise RuntimeError(f"Failed to load models: {str(e)}")

        # Convert gender to binary
        gender_binary = 1 if gender.lower() == 'perempuan' else 0

        # List of original 4 program studi
        original_programs = [
            'S1 Teknik Informatika - Kampus Purwokerto',
            'S1 Sistem Informasi - Kampus Purwokerto',
            'S1 Rekayasa Perangkat Lunak - Kampus Purwokerto',
            'S1 Sains Data - Kampus Purwokerto'
        ]

        # Map unseen program studi to S1 Rekayasa Perangkat Lunak - Kampus Purwokerto
        if program_studi not in original_programs:
            mapped_program_studi = 'S1 Rekayasa Perangkat Lunak - Kampus Purwokerto'
        else:
            mapped_program_studi = program_studi

        # Create input data
        data = {
            'Sem 1': processed_semesters['Sem 1'],
            'Sem 2': processed_semesters['Sem 2'],
            'Sem 3': processed_semesters['Sem 3'],
            'Sem 4': processed_semesters['Sem 4'],
            'rata2_IPS': rata2_IPS,
            'predicted_gender': gender_binary,
            'program_studi': mapped_program_studi
        }

        # Convert to DataFrame
        df = pd.DataFrame([data])

        try:
            # Apply label encoding for program studi
            df['program_studi_le'] = le_program_studi.transform(df['program_studi'].astype(str))
        except Exception as e:
            raise ValueError(f"Invalid program studi: {program_studi}") from e

        # Prepare features for classification (no scaling)
        classification_features = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'rata2_IPS', 'predicted_gender', 'program_studi_le']
        X_classification = df[classification_features]

        # Make classification prediction
        classification_pred = classification_model.predict(X_classification)[0]
        classification_proba = classification_model.predict_proba(X_classification)[0]

        # Prepare features for regression (without scaling)
        regression_features = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'rata2_IPS', 'predicted_gender', 'program_studi_le']
        X_regression = df[regression_features]

        # Make regression prediction
        regression_pred = regression_model.predict(X_regression)[0]
        
        # Adjust regression prediction based on program type and classification
        if mapped_program_studi == 'D3 Teknik Telekomunikasi':
            # Apply reduction for D3 programs first
            regression_pred = regression_pred - 2

            if classification_pred == 1:  # D3 and On Time
                regression_pred = 6 # Force to 6 semesters
            else: # D3 and At Risk to Graduate Late
                # Cap D3 At Risk students between 6 and 10 semesters
                regression_pred = min(max(regression_pred, 6), 10)
        else: # S1 Programs
            if classification_pred == 1:  # S1 and On Time
                # S1 programs capped between 7 and 8
                regression_pred = min(max(regression_pred, 7), 8)
            # else: # S1 and At Risk to Graduate Late
                # For S1 At Risk, no specific cap, use model's prediction as is
                # (This is implicitly handled by not having an 'else' block here)

        # Prepare response
        result = {
            'classification': {
                'status': 'Likely to Graduate on Time' if classification_pred == 1 else 'At Risk to Graduate Late',
                'probability': float(classification_proba[classification_pred])
            },
            'regression': {
                'predicted_semester': float(regression_pred)
            },
            'recommendation': get_recommendation(classification_pred, data)
        }

        print(json.dumps(result))
        return 0

    except Exception as e:
        error_msg = f"Error in prediction: {str(e)}\n{traceback.format_exc()}"
        print(error_msg, file=sys.stderr)
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
    if len(sys.argv) != 7:
        print("Usage: python predict.py <sem1> <sem2> <sem3> <sem4> <gender> <program_studi>", file=sys.stderr)
        sys.exit(1)

    sys.exit(predict(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])) 