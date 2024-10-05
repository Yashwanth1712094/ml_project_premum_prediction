import streamlit as st
from prediction_helper import predict
# Title for the app
st.title("Health Insurance Data Input Form")



# Create three columns
col1, col2, col3 = st.columns(3)
# Distribute the input fields across the columns

# Column 1
with col1:
    age = st.number_input("Age", min_value=18, max_value=100)
    gender = st.selectbox("Gender", ['Male', 'Female'])
    marital_status = st.selectbox("Marital Status", ['Unmarried', 'Married'])
    employment_status = st.selectbox("Employment Status", ['Salaried', 'Self-Employed', 'Freelancer'])

# Column 2
with col2:
    region = st.selectbox("Region", ['Northwest', 'Southeast', 'Northeast', 'Southwest'])
    bmi_category = st.selectbox("BMI Category", ['Normal', 'Obesity', 'Overweight', 'Underweight'])
    income_lakhs = st.number_input('Income in Lakhs', step=1, min_value=0, max_value=200)
    genetical_risk = st.number_input("Genetical Risk", min_value=0, max_value=100)

# Column 3
with col3:
    smoking_status = st.selectbox("Smoking Status", [
        'No Smoking', 'Regular', 'Occasional', 'Does Not Smoke', 
        'Not Smoking', 'Smoking=0'
    ])
    medical_history = st.selectbox("Medical History", [
        'Diabetes', 'High blood pressure', 'No Disease', 
        'Diabetes & High blood pressure', 'Thyroid', 'Heart disease',
        'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ])
    insurance_plan = st.selectbox("Insurance Plan", ['Bronze', 'Silver', 'Gold'])
    number_of_dependants=st.number_input('Number of Dependants',min_value=0,max_value=5)

input_dict={
    'Age':age,
    'Gender': gender,
 'Region': region,
 'Marital_status': marital_status,
 'Bmi_category': bmi_category,
 'Smoking_status': smoking_status,
 'Employment_status': employment_status,
 'Income_lakhs': income_lakhs,
 'Medical_history': medical_history,
 'Insurance_plan': insurance_plan,
 'Genetical_risk': genetical_risk,
 'Number of Depenants':number_of_dependants,
 }

if st.button('Predict'):
    prediction=predict(input_dict)
    st.success(f"Predicted premum:{prediction}")