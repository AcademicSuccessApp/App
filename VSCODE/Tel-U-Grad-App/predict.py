import sys
import json
import joblib
import numpy as np
import pandas as pd
import traceback

def predict(sem1, sem2, sem3, sem4, gender, program_studi):
    try:
        print(f"DEBUG: Received inputs - sem1={sem1}, sem2={sem2}, sem3={sem3}, sem4={sem4}, gender={gender}, program_studi={program_studi}", file=sys.stderr)

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
        print(f"DEBUG: processed_semesters={processed_semesters}, rata2_IPS={rata2_IPS}", file=sys.stderr)

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
        print(f"DEBUG: mapped_program_studi={mapped_program_studi}", file=sys.stderr)

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
        print(f"DEBUG: DataFrame before encoding=\n{df}", file=sys.stderr)

        try:
            # Apply label encoding for program studi
            df['program_studi_le'] = le_program_studi.transform(df['program_studi'].astype(str))
        except Exception as e:
            raise ValueError(f"Invalid program studi: {program_studi}") from e
        print(f"DEBUG: DataFrame after encoding=\n{df}", file=sys.stderr)

        # Prepare features for classification (no scaling)
        classification_features = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'rata2_IPS', 'predicted_gender', 'program_studi_le']
        X_classification = df[classification_features]
        print(f"DEBUG: X_classification=\n{X_classification}", file=sys.stderr)

        # Make classification prediction
        classification_pred = classification_model.predict(X_classification)[0]
        classification_proba = classification_model.predict_proba(X_classification)[0]
        print(f"DEBUG: classification_pred={classification_pred}, classification_proba={classification_proba}", file=sys.stderr)

        # Prepare features for regression (without scaling)
        regression_features = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'rata2_IPS', 'predicted_gender', 'program_studi_le']
        X_regression = df[regression_features]
        print(f"DEBUG: X_regression=\n{X_regression}", file=sys.stderr)

        # Make regression prediction
        regression_pred = regression_model.predict(X_regression)[0]
        print(f"DEBUG: raw regression_pred={regression_pred}", file=sys.stderr)
        
        # Special condition: If all IPS are 4.0, predict fastest graduation
        all_ips_perfect = all(val == 4.0 for val in processed_semesters.values())
        print(f"DEBUG: all_ips_perfect={all_ips_perfect}", file=sys.stderr)

        if all_ips_perfect:
            # Use the original program_studi for this logic branch
            if program_studi == 'D3 Teknik Telekomunikasi': # Check original program_studi
                regression_pred = 6.0
                print(f"DEBUG: Perfect IPS, D3 (original), setting regression_pred={regression_pred}", file=sys.stderr)
            else:
                regression_pred = 7.0 # Fastest for S1
                print(f"DEBUG: Perfect IPS, S1 (original), setting regression_pred={regression_pred}", file=sys.stderr)
            classification_pred = 1 # Force to 'Likely to Graduate on Time'
            classification_proba = np.array([0.0, 1.0]) # Assume 100% confidence for class 1
            print(f"DEBUG: Perfect IPS, forcing classification_pred={classification_pred}, classification_proba={classification_proba}", file=sys.stderr)

        # Adjust regression prediction based on program type and classification
        # Use the original program_studi for this logic branch
        if program_studi == 'D3 Teknik Telekomunikasi': # Check original program_studi
            print(f"DEBUG: Entering D3-specific adjustment (original). Current regression_pred={regression_pred}", file=sys.stderr)
            # Apply reduction for D3 programs first (only if not already set by perfect IPS condition)
            if not all_ips_perfect:
                regression_pred = regression_pred - 2
                print(f"DEBUG: D3 (original) not perfect IPS, reduced regression_pred={regression_pred}", file=sys.stderr)

            if classification_pred == 1:  # D3 and On Time
                if regression_pred != 6: # Check if it was already set to 6 by perfect IPS
                    regression_pred = 6 # Force to 6 semesters
                    print(f"DEBUG: D3 (original) On Time, forced regression_pred={regression_pred}", file=sys.stderr)
            else: # D3 and At Risk to Graduate Late
                # Cap D3 At Risk students between 6 and 10 semesters
                regression_pred = min(max(regression_pred, 6), 10)
                print(f"DEBUG: D3 (original) At Risk, capped regression_pred={regression_pred}", file=sys.stderr)
        else: # S1 Programs (or other non-D3)
            print(f"DEBUG: Entering S1-specific adjustment (original). Current regression_pred={regression_pred}", file=sys.stderr)
            if classification_pred == 1:  # S1 and On Time
                # S1 programs capped between 7 and 8 (only if not already set by perfect IPS condition)
                if not all_ips_perfect:
                    regression_pred = min(max(regression_pred, 7), 8)
                    print(f"DEBUG: S1 (original) On Time, not perfect IPS, capped regression_pred={regression_pred}", file=sys.stderr)
            else: # S1 and At Risk to Graduate Late
                print(f"DEBUG: S1 (original) At Risk, using model prediction as is.", file=sys.stderr)

        print(f"DEBUG: Final regression_pred={regression_pred}", file=sys.stderr)
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