# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote
import random

# ==============
# CONFIGURATION
# ==============
st.set_page_config(
    page_title="Stirling Q&R Lead Generation",
    page_icon="📈",
    layout="centered"
)

# Simplified color scheme for better contrast
COLORS = {
    "primary": "#387E2E",  # Dark green
    "secondary": "#6BC651",  # Medium green
    "background": "#FFFFFF",  # Pure white
    "text": "#0E1116",  # Dark gray
    "border": "#F0F0F0"  # Light gray
}

# GitHub configuration
GITHUB_USER = "StirlingQR"
REPO_NAME = "Lead-Gen"
BRANCH = "main"
PDF_FILENAME = "Top 5 Considerations Before Signing an Exclusive Agency Agreement.pdf"
ENCODED_FILENAME = quote(PDF_FILENAME)
PDF_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ENCODED_FILENAME}"

# ==============
# CUSTOM STYLES
# ==============
st.markdown(f"""
<style>
    body {{
        color: {COLORS['text']};
    }}
    .stApp {{
        background-color: {COLORS['background']};
    }}
    .main-container {{
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 2rem;
        margin: 1rem 0;
    }}
    .stButton>button {{
        background-color: {COLORS['primary']} !important;
        color: white !important;
        border-radius: 4px;
    }}
    .stButton>button:hover {{
        background-color: {COLORS['secondary']} !important;
    }}
    .logo-container {{
        text-align: center;
        margin: 1rem 0;
    }}
    .consent-text {{
        font-size: 0.9em;
        color: #666666;
        margin-top: 1rem;
    }}
</style>
""", unsafe_allow_html=True)

# ==============
# COMPONENTS
# ==============
def display_logo():
    try:
        st.markdown("""
        <div class="logo-container">
            <img src="https://raw.githubusercontent.com/StirlingQR/Lead-Gen/main/Stirling_QR_Logo.png" 
                 style="height: 80px; margin-bottom: 1rem;">
        </div>
        """, unsafe_allow_html=True)
    except:
        st.error("Logo loading issue - proceeding without logo")

# Rest of the code remains similar but with updated color references
# [Keep previous functionality for lead management, CAPTCHA, etc]

# ==============
# CONSENT TEXT
# ==============
consent_markdown = """
<div class="consent-text">
<p>By submitting this form, you:</p>
<ul>
<li>Grant Stirling Q&R explicit permission to contact you via the provided contact details</li>
<li>Acknowledge that your information will be stored securely in our systems</li>
<li>Agree to our legitimate business interest in processing your data</li>
<li>Understand you may withdraw consent at any time by contacting talent@stirlingqr.com</li>
</ul>
</div>
"""

# In your form section:
with st.form("lead_form", clear_on_submit=True):
    # ... form fields ...
    st.markdown(consent_markdown, unsafe_allow_html=True)
    submitted = st.form_submit_button("Get Your Copy Now →")
