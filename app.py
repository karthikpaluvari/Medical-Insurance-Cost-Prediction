# app.py
# 💊 Smart Medical Insurance Cost Predictor (India 🇮🇳)
# Updated version: with Health, Lifestyle & Family inputs

import streamlit as st
import pickle
import os
import numpy as np
import pandas as pd

# -------------------------------
# 🧠 Page Setup
# -------------------------------
st.set_page_config(page_title="Medical Insurance Cost Prediction", page_icon="💊")

st.title("💊 Medical Insurance Cost Prediction 🇮🇳")
st.write(
    "Compare **real Indian health insurance plans** and their estimated annual premiums "
    "based on your personal, health, and lifestyle details."
)

# -------------------------------
# 📦 Load Model
# -------------------------------
model_file = None
for f in ["insurance_model.pkl", "insurance_model_backup.pkl"]:
    if os.path.exists(f):
        model_file = f
        break

if model_file is None:
    st.error("❌ Model file not found. Please train the model first (`python train_model.py`).")
    st.stop()

with open(model_file, "rb") as f:
    model = pickle.load(f)

st.success("✅ Model loaded successfully!")

# -------------------------------
# 🧍 Personal Details (Original)
# -------------------------------
st.header("🧍 Enter Your Details")

age = st.slider("Age", 18, 100, 30)
sex = st.selectbox("Sex", ("Male", "Female"))
bmi = st.number_input("BMI (Body Mass Index)", 10.0, 50.0, 25.0)
children = st.selectbox("Number of Children", (0, 1, 2, 3, 4, 5))
smoker = st.selectbox("Smoker", ("Yes", "No"))
city = st.selectbox(
    "City",
    ("Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"),
)

# -------------------------------
# 🏥 Health & Medical Factors
# -------------------------------
st.header("🏥 Health & Medical Factors")
blood_pressure = st.selectbox("Blood Pressure Level", ["Normal", "High", "Very High"])
cholesterol = st.selectbox("Cholesterol Level", ["Normal", "Borderline", "High"])
diabetes = st.radio("Do you have Diabetes?", ["No", "Yes"])
heart_disease = st.radio("Any Heart Disease History?", ["No", "Yes"])
asthma = st.radio("Asthma / Lung Condition?", ["No", "Yes"])
thyroid = st.radio("Thyroid / Hormonal Disorder?", ["No", "Yes"])
medications = st.text_input("Medications in Use (if any)", placeholder="e.g., BP medicine")
disability = st.radio("Disability Status", ["No", "Yes"])

# -------------------------------
# 🏃‍♀️ Lifestyle & Habits
# -------------------------------
st.header("🏃‍♀️ Lifestyle & Habits")
alcohol = st.selectbox("Alcohol Consumption", ["None", "Occasional", "Regular"])
exercise = st.selectbox("Exercise Frequency", ["Daily", "Weekly", "Rarely"])
sleep_hours = st.number_input("Average Sleep Hours per Day", min_value=0, max_value=24, step=1)
diet = st.selectbox("Diet Type", ["Vegetarian", "Non-Veg", "Mixed"])
stress = st.selectbox("Stress Level", ["Low", "Moderate", "High"])
work_env = st.selectbox("Work Environment", ["Office", "Field", "Hazardous"])

# -------------------------------
# 👨‍👩‍👧‍👦 Family & Dependents
# -------------------------------
st.header("👨‍👩‍👧‍👦 Family & Dependents")
family_history = st.selectbox("Family History of Diseases", ["None", "Minor", "Major"])
parents_covered = st.radio("Are Parents Already Covered?", ["No", "Yes"])

# -------------------------------
# 🔢 Encode Inputs
# -------------------------------
sex_val = 1 if sex == "Male" else 0
smoker_val = 1 if smoker == "Yes" else 0
city_map = {
    "Delhi": 0, "Mumbai": 1, "Bengaluru": 2, "Hyderabad": 3,
    "Chennai": 4, "Kolkata": 5, "Pune": 6, "Ahmedabad": 7,
}
city_value = city_map[city]
city_multiplier = {
    "Delhi": 1.2, "Mumbai": 1.3, "Bengaluru": 1.1, "Hyderabad": 1.0,
    "Chennai": 0.95, "Kolkata": 0.9, "Pune": 1.0, "Ahmedabad": 0.85,
}

# -------------------------------
# 🏦 Insurance Plan Data
# -------------------------------
plans = {
    "Care Health Protect Plus": {
        "multiplier": 0.8,
        "benefits": [
            "✅ ₹5L hospitalization cover",
            "✅ Free annual health checkup",
            "✅ Pre and post-hospitalization up to 60 days",
            "✅ Lifetime renewability",
            "❌ No international coverage",
        ],
    },
    "Star Health Family Optima": {
        "multiplier": 1.0,
        "benefits": [
            "✅ ₹10L family cover (2 adults + 2 kids)",
            "✅ No pre-policy medical test required",
            "✅ Cashless treatment in 12,000+ hospitals",
            "✅ Free annual health checkup for all members",
            "✅ Coverage for AYUSH treatments",
        ],
    },
    "HDFC ERGO Health Suraksha": {
        "multiplier": 1.15,
        "benefits": [
            "✅ ₹15L sum insured",
            "✅ Maternity & newborn cover after 2 years",
            "✅ Daily hospital cash benefit",
            "✅ Free health coach & teleconsultation",
            "✅ No room rent limit",
        ],
    },
    "ICICI Lombard Complete Health": {
        "multiplier": 1.25,
        "benefits": [
            "✅ ₹20L sum insured",
            "✅ Critical illness and major surgery cover",
            "✅ Free annual health check-up",
            "✅ Cashless hospital network (7,500+ hospitals)",
            "✅ Complimentary wellness programs",
        ],
    },
    "Aditya Birla Active Fit": {
        "multiplier": 1.35,
        "benefits": [
            "✅ ₹25L coverage with wellness rewards",
            "✅ Includes fitness & diet programs",
            "✅ International emergency assistance",
            "✅ Critical illness & accident cover",
            "✅ Earn cashback for healthy lifestyle",
        ],
    },
}

# -------------------------------
# 🔮 Prediction Logic
# -------------------------------
if st.button("🔍 Show All Available Plans"):
    input_data = np.array([[age, sex_val, bmi, children, smoker_val, city_value]])
    base_prediction = model.predict(input_data)[0]
    base_inr = base_prediction * 8.4  # Convert USD→INR scaling

    # 🧠 Apply extra modifiers based on health & lifestyle
    multiplier = 1.0

    # Health modifiers
    if blood_pressure == "High": multiplier += 0.10
    elif blood_pressure == "Very High": multiplier += 0.20
    if cholesterol == "Borderline": multiplier += 0.05
    elif cholesterol == "High": multiplier += 0.10
    if diabetes == "Yes": multiplier += 0.15
    if heart_disease == "Yes": multiplier += 0.20
    if asthma == "Yes": multiplier += 0.05
    if thyroid == "Yes": multiplier += 0.05
    if disability == "Yes": multiplier += 0.10

    # Lifestyle modifiers
    if alcohol == "Occasional": multiplier += 0.05
    elif alcohol == "Regular": multiplier += 0.10
    if exercise == "Rarely": multiplier += 0.05
    if stress == "High": multiplier += 0.10
    if work_env == "Hazardous": multiplier += 0.10

    # Family modifiers
    if family_history == "Minor": multiplier += 0.05
    elif family_history == "Major": multiplier += 0.10

    adjusted_prediction = base_inr * city_multiplier[city] * multiplier

    # 🏦 Display All Plans
    results = []
    for plan_name, info in plans.items():
        cost = adjusted_prediction * info["multiplier"]
        benefits_text = "\n".join(info["benefits"])
        results.append([plan_name, cost, benefits_text])

    df = pd.DataFrame(results, columns=["Insurance Plan", "Estimated Annual Premium (₹)", "Key Benefits"])
    df = df.sort_values(by="Estimated Annual Premium (₹)")
    df["Estimated Annual Premium (₹)"] = df["Estimated Annual Premium (₹)"].apply(lambda x: f"₹ {x:,.2f}")

    st.subheader(f"📊 Available Insurance Plans in {city}")
    for _, row in df.iterrows():
        st.markdown(f"### 🏦 {row['Insurance Plan']}")
        st.write(f"💰 **Estimated Premium:** {row['Estimated Annual Premium (₹)']} per year")
        st.markdown("**Key Benefits:**")
        for line in row["Key Benefits"].split("\n"):
            st.write(line)
        st.markdown("---")

    # 🎯 Recommendation
    recommended = df.iloc[1]["Insurance Plan"] if smoker_val else df.iloc[0]["Insurance Plan"]
    st.success(f"🎯 Recommended Plan for You: **{recommended}**")

    st.markdown("---")
    st.caption(
        f"🏙️ City: {city} ×{city_multiplier[city]} | 🧠 Smoker: {'Yes' if smoker_val else 'No'} | Age: {age} | Lifestyle multiplier: {multiplier:.2f}"
    )
    st.caption("*(Based on ML prediction adjusted for Indian insurance cost levels and health profile)*")

st.markdown("---")
st.caption("Developed by Karthik | AIML Mini Project 2025 | 🇮🇳")
