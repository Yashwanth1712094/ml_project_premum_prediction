from joblib import load
import pandas as pd

model_rest=load('artifacts/model_rest.joblib')
model_young=load('artifacts/model_young.joblib')
scalar_rest=load('artifacts/scaler_rest.joblib')
scalar_young=load('artifacts/scaler_young.joblib')



import pandas as pd

def calculate_normalized_risk_score(medical_history):
    risk_scores = {
    "diabetes": 6,
    "heart disease": 8,
    "high blood pressure": 6,
    "thyroid": 5,
    "no disease": 0,
    "none": 0
}
    diseases = medical_history.lower().split(" & ")

    # Calculate the total risk score by summing the risk scores for each part
    total_risk_score = sum(risk_scores.get(disease, 0) for disease in diseases)  # Default to 0 if disease not found

    max_score = 14 # risk score for heart disease (8) + second max risk score (6) for diabetes or high blood pressure
    min_score = 0  # Since the minimum score is always 0

    # Normalize the total risk score
    normalized_risk_score = (total_risk_score - min_score) / (max_score - min_score)

    return normalized_risk_score


# Define the risk scores dictionary


# Example usage
medical_history_input = "Diabetes & Heart disease"
normalized_risk_score = calculate_normalized_risk_score(medical_history_input)

print(f"Medical History: {medical_history_input}")
print(f"Normalized Risk Score: {normalized_risk_score:.2f}")


def preprocess_input(input_dict):
    expected_columns=['age', 'number_of_dependants', 'income_lakhs', 'insurance_plan',
       'genetical_risk', 'normalized_score', 'gender_Male', 'region_Northwest',
       'region_Southeast', 'region_Southwest', 'marital_status_Unmarried',
       'bmi_category_Obesity', 'bmi_category_Overweight',
       'bmi_category_Underweight', 'smoking_status_Occasional',
       'smoking_status_Regular', 'employment_status_Salaried',
       'employment_status_Self-Employed']
    print("expected_columns done")

    insurance_plan_encoding={'Bronze':1,'Silver':2,'Gold':3}
    df=pd.DataFrame(0,columns=expected_columns,index=[0])

    for key, value in input_dict.items():
        if key == 'Gender' and value == 'Male':
            df['gender_Male'] = 1
        elif key == 'Region':
            if value == 'Northwest':
                df['region_Northwest'] = 1
            elif value == 'Southeast':
                df['region_Southeast'] = 1
            elif value == 'Southwest':
                df['region_Southwest'] = 1
        elif key == 'Marital_Status' and value == 'Unmarried':
            df['marital_status_Unmarried'] = 1
        elif key == 'Bmi_category':
            if value == 'Obesity':
                df['bmi_category_Obesity'] = 1
            elif value == 'Overweight':
                df['bmi_category_Overweight'] = 1
            elif value == 'Underweight':
                df['bmi_category_Underweight'] = 1
        elif key == 'Smoking_status':
            if value == 'Occasional':
                df['smoking_status_Occasional'] = 1
            elif value == 'Regular':
                df['smoking_status_Regular'] = 1
        elif key == 'Employment_status':
            if value == 'Salaried':
                df['employment_status_Salaried'] = 1
            elif value == 'Self-Employed':
                df['employment_status_Self-Employed'] = 1
        elif key == 'Insurance_plan':  # Correct key usage with case sensitivity
            df['insurance_plan'] = insurance_plan_encoding[value]
        elif key == 'Age':  # Correct key usage with case sensitivity
            df['age'] = value
        elif key == 'Number of Dependants':  # Correct key usage with case sensitivity
            df['number_of_dependants'] = value
        elif key == 'Income_lakhs':  # Correct key usage with case sensitivity
            df['income_lakhs'] = value
        elif key == "Genetical_risk":
            df['genetical_risk'] = value
    print("key value done")
    df['normalized_score']=calculate_normalized_risk_score(input_dict['Medical_history'])
    print("noralized risk score done")
    df=handle_scaling(input_dict['Age'],df)
    df=df[expected_columns]
    return df

def handle_scaling(age,df):
    if age<=25:
        scalar_object=scalar_young
    else:
        scalar_object=scalar_rest

    cols_to_scale=scalar_object['cols_to_scale']
    scalar=scalar_object['scaler']
    
    print(cols_to_scale)
    # df['income_level'] = None # since scaler object expects income_level supply it. This will have no impact on anything
    # df[cols_to_scale] = scalar.transform(df[cols_to_scale])
    

    return df

def predict(input_dict): 
    input_df=preprocess_input(input_dict)

    if(input_dict['Age']<=25):
        prediction=model_young.predict(input_df)

    else:
        prediction=model_rest.predict(input_df)

    return int(prediction)