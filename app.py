import base64
import glob
import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Internet Scavenger - E-commerce Trends",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 Internet Scavenger")
st.subheader("Top Trending Products Across Amazon and Etsy")

# --- BULLETPROOF LOCAL IMAGE FINDER & DEBUGGER ---
script_dir = os.path.dirname(os.path.abspath(__file__))
all_files_in_dir = os.listdir(script_dir)

img_base64 = ""
IMAGE_PATH = None

# Look for globe file explicitly ignoring case
for f in all_files_in_dir:
  if "globe" in f.lower() and f.lower().endswith((".jpg", ".jpeg", ".png")):
    IMAGE_PATH = os.path.join(script_dir, f)
    break

if IMAGE_PATH and os.path.exists(IMAGE_PATH):
  with open(IMAGE_PATH, "rb") as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode()

# --- ROTATING EXACT GLOBE COMPONENT ---
if img_base64:
  globe_html = f"""
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin: 10px 0;">
        <div class="globe-wrapper">
            <img src="data:image/jpeg;base64,{img_base64}" class="rotating-globe">
        </div>
    </div>

    <style>
        .globe-wrapper {{
            width: 220px;
            height: 220px;
            border-radius: 50%;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: inset -20px -15px 30px rgba(0, 0, 0, 0.8), 
                        0 0 20px rgba(0, 0, 0, 0.6);
        }}
        .rotating-globe {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 50%;
            animation: spin 20s linear infinite;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    """
  st.components.v1.html(globe_html, height=250)
else:
  st.error(
      f"⚠️ Image not found. Python is looking inside: `{script_dir}`. Files"
      f" found there: {all_files_in_dir}"
  )
