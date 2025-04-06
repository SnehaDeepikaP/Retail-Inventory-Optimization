import streamlit as st
import subprocess
import json
import re

def run_pricing_optimizer():
    try:
        result = subprocess.run("ollama run llama3.2 < pricing_prompt.txt", 
                                capture_output=True, text=True, shell=True)

        with open("pricing_output_raw.txt", "w", encoding="utf-8") as raw_file:
            raw_file.write(result.stdout)

        return result.stdout
    except Exception as e:
        return str(e)

def extract_valid_json(text):
    match = re.search(r'\[\s*{.*?}\s*]', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError as e:
            st.error(f"⚠️ JSON error: {e}")
            return None
    return None

# Streamlit UI
st.set_page_config(page_title="Pricing Optimization", layout="centered")
st.title("💰 Pricing Optimization Dashboard")

if st.button("📈 Optimize Prices"):
    st.info("Running Pricing Optimization Agent...")
    output = run_pricing_optimizer()

    json_data = extract_valid_json(output)

    if json_data:
        with open("pricing_output.json", "w") as json_file:
            json.dump(json_data, json_file, indent=2)

        st.success("✅ Pricing recommendations generated!")
        st.json(json_data)
    else:
        st.error("❌ JSON parsing failed. See `pricing_output_raw.txt` for model output.")
