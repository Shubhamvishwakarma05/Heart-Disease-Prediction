import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Load the trained model
with open('heart_disease_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Set page configuration
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="💓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styles for better UI
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
        color: #333;
    }
    h1, h2, h3 {
        color: #FF4B4B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header
st.image("https://via.placeholder.com/800x200.png?text=Heart+Health", use_column_width=True)
st.markdown("## **Heart Disease Prediction App 💓**")
st.markdown("### **Predict the likelihood of heart disease based on patient details.**")
st.markdown(
    """
    **About the App**:
    - Provide your health details to predict the likelihood of heart disease.
    - Visualize results through interactive charts.
    - Learn more about symptoms and precautions for heart disease at the end.
    """
)

# Sidebar for input
st.sidebar.header("Patient Input Details")
st.sidebar.markdown("Provide the necessary patient details to make a prediction.")

# Input fields
age = st.sidebar.number_input("Age (years)", min_value=0, max_value=120, value=50)
sex = st.sidebar.selectbox("Gender", options=["Female", "Male"])
anaemia = st.sidebar.selectbox("Anaemia (Low Red Blood Cells)", options=["No", "Yes"])
creatinine_phosphokinase = st.sidebar.number_input("CPK Enzyme Level (mcg/L)", min_value=0, max_value=10000, value=250)
diabetes = st.sidebar.selectbox("Diabetes", options=["No", "Yes"])
ejection_fraction = st.sidebar.slider("Ejection Fraction (%)", min_value=0, max_value=100, value=50)
high_blood_pressure = st.sidebar.selectbox("High Blood Pressure", options=["No", "Yes"])
platelets = st.sidebar.number_input("Platelets Count (kiloplatelets/mL)", min_value=0.0, max_value=1000000.0, value=250000.0)
serum_creatinine = st.sidebar.number_input("Serum Creatinine Level (mg/dL)", min_value=0.0, max_value=10.0, value=1.0)
serum_sodium = st.sidebar.slider("Serum Sodium Level (mEq/L)", min_value=100, max_value=150, value=135)
smoking = st.sidebar.selectbox("Smoking", options=["No", "Yes"])
time = st.sidebar.number_input("Follow-up Period (days)", min_value=0, max_value=500, value=150)

# Convert categorical inputs to numerical
sex = 1 if sex == "Male" else 0
anaemia = 1 if anaemia == "Yes" else 0
diabetes = 1 if diabetes == "Yes" else 0
high_blood_pressure = 1 if high_blood_pressure == "Yes" else 0
smoking = 1 if smoking == "Yes" else 0

# Predict Button
if st.sidebar.button("Predict"):
    # Prepare input data
    input_data = np.array([[age, anaemia, creatinine_phosphokinase, diabetes,
                            ejection_fraction, high_blood_pressure, platelets,
                            serum_creatinine, serum_sodium, sex, smoking, time]])

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Result Display
    st.subheader("Prediction Results")
    if prediction == 1:
        st.error("The model predicts that the patient is **at risk of heart disease.**")
    else:
        st.success("The model predicts that the patient is **not at risk of heart disease.**")

    # Visual Feedback
    risk = [70, 30] if prediction == 1 else [30, 70]
    labels = ['At Risk', 'Healthy']
    colors = ['red', 'green']
    fig, ax = plt.subplots()
    ax.pie(risk, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# Feature Explanations
st.markdown("### **Feature Explanations**")
feature_info = {
    "Age": "Patient's age in years.",
    "Gender": "Biological sex of the patient.",
    "Anaemia": "Indicates if the patient has low levels of red blood cells.",
    "CPK": "Level of creatinine phosphokinase enzyme in the blood.",
    "Diabetes": "Indicates if the patient has diabetes.",
    "Ejection Fraction": "Percentage of blood leaving the heart during a contraction.",
    "High Blood Pressure": "Indicates if the patient has hypertension.",
    "Platelets": "Platelets in blood (kiloplatelets per mL).",
    "Serum Creatinine": "Creatinine levels in the blood (mg/dL).",
    "Serum Sodium": "Sodium levels in the blood (mEq/L).",
    "Smoking": "Indicates if the patient is a smoker.",
    "Follow-up Period": "Days since the patient was last seen by the doctor.",
}
for feature, explanation in feature_info.items():
    st.markdown(f"**{feature}:** {explanation}")

# Heart Disease Information
st.markdown("### **Heart Disease Information**")
st.markdown(
    """
    **Symptoms**:
    - Chest pain or discomfort.
    - Shortness of breath.
    - Fatigue, lightheadedness, or dizziness.
    - Pain in the neck, jaw, throat, or back.

    **Precautions**:
    - Maintain a healthy diet.
    - Exercise regularly (at least 30 minutes daily).
    - Avoid smoking and excessive alcohol.
    - Manage stress and get enough sleep.
    - Regularly check blood pressure, cholesterol, and glucose levels.
    """
)
st.markdown("---")
st.markdown("💡 **Tip**: Early detection and lifestyle changes are key to preventing heart disease.")

