import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

models = genai.list_models()

for m in models:
    print(m.name, "->", m.supported_generation_methods)
