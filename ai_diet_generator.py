import google.generativeai as genai
import json
import streamlit as st

# ==============================
# Gemini Configuration
# ==============================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ CORRECT MODEL (NO models/)
model = genai.GenerativeModel("gemini-1.5-flash")

# ==============================
# Diet Generator Function
# ==============================
def generate_diet(patient_id):
    with open("final_diet_output.json", "r") as f:
        patients = json.load(f)

    patient = next((p for p in patients if p["patient_id"] == patient_id), None)
    if not patient:
        return None

    disease = patient["bert_prediction"]

    prompt = f"""
You are a clinical dietitian.

Generate a 2-day diet plan.

Patient ID: {patient_id}
Medical Condition: {disease}

FORMAT:

Day 1:
Breakfast:
Lunch:
Snack:
Dinner:

Day 2:
Breakfast:
Lunch:
Snack:
Dinner:
"""

    response = model.generate_content(prompt)
    return response.text
