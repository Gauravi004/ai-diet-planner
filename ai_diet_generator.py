import google.generativeai as genai
import json
import os

# ---------- CONFIG ----------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- FUNCTION ----------
def generate_diet(patient_id):

    with open("final_diet_output.json", "r") as f:
        patients = json.load(f)

    patient = next((p for p in patients if p["patient_id"] == patient_id), None)
    if not patient:
        return None

    disease = patient["bert_prediction"]

    prompt = f"""
You are a clinical dietitian.

Generate a 2-day diet plan for the following patient.

Patient ID: {patient_id}
Medical Condition: {disease}

IMPORTANT RULES:
- Mention ONLY ONE disease.
- Use EXACTLY the format shown below.
- Keep meals simple and realistic.
- No explanations, no tables.

FORMAT:

Patient: {patient_id}

Medical Condition: {disease}

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

    return {
        "patient_id": patient_id,
        "bert_prediction": disease,
        "diet_plan": response.text
    }
