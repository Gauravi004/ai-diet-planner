import json
from google import genai

# ---------- CONFIG ----------
client = genai.Client(
    api_key="AIzaSyCY2-GoFn-5sRYHj5fU8qACivH5eDY-cqs"
)

# ---------- FUNCTION ----------
def generate_diet(patient_id):

    # Load patient predictions
    with open("final_diet_output.json", "r") as f:
        patients = json.load(f)

    # Find patient
    patient = next(
        (p for p in patients if p["patient_id"] == patient_id),
        None
    )

    if not patient:
        return None

    disease = patient["bert_prediction"]

    # ---------- PROMPT ----------
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

    # ---------- AI CALL ----------
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )

    # ---------- RETURN (VERY IMPORTANT) ----------
    return {
        "patient_id": patient_id,
        "bert_prediction": disease,
        "diet_plan": response.text
    }
