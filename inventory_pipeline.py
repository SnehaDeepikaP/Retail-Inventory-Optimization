import streamlit as st
import subprocess
import json
import re
import os

def run_inventory_monitor():
    try:
        result = subprocess.run("ollama run llama3.2 < inventory_prompt.txt", 
                                capture_output=True, text=True, shell=True)

        with open("inventory_output_raw.txt", "w", encoding="utf-8") as raw_file:
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

# Streamlit Dashboard
st.set_page_config(page_title="Inventory Monitor", layout="centered")
st.title("📦 Inventory Monitoring Dashboard")

if st.button("🔍 Monitor Inventory"):
    st.info("Running Inventory Monitoring Agent...")
    output = run_inventory_monitor()

    json_data = extract_valid_json(output)

    if json_data:
        with open("inventory_output.json", "w") as json_file:
            json.dump(json_data, json_file, indent=2)

        st.success("✅ Inventory status loaded successfully!")
        st.json(json_data)
    else:
        st.error("❌ Could not parse valid JSON. Check `inventory_output_raw.txt`.")
