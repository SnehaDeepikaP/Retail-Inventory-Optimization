import streamlit as st
import subprocess
import json
import re

def run_forecast():
    try:
        result = subprocess.run(["ollama", "run", "llama3.2", "<", "forecast_prompt.txt"],
                                capture_output=True, text=True, shell=True)
        with open("forecast_output_raw.txt", "w", encoding="utf-8") as raw_file:
            raw_file.write(result.stdout)
        return result.stdout
    except Exception as e:
        return str(e)

def extract_valid_json(text):
    # Find first valid JSON object or array using regex
    match = re.search(r'({.*?}|\[.*?\])', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            st.error("⚠️ JSON structure found, but still invalid content.")
            return None
    return None

st.set_page_config(page_title="Demand Forecast", layout="centered")
st.title("📊 Retail Demand Forecast Dashboard")

if st.button("🚀 Run Forecast"):
    st.info("Running Ollama model and generating forecast...")
    output = run_forecast()
    st.success("Forecast complete! Output saved.")

    json_data = extract_valid_json(output)

    if json_data:
        st.success("✅ JSON loaded successfully!")
        st.json(json_data)
    else:
        st.error("❌ Could not parse JSON output. Please check the forecast output.")
