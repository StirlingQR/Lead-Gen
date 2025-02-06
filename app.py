# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote
import random

# Configure page
st.set_page_config(
    page_title="Stirling Q&R Lead Generation",
    page_icon="📈",
    layout="centered"
)

# GitHub configuration
GITHUB_USER = "StirlingQR"
REPO_NAME = "Lead-Gen"
BRANCH = "main"
PDF_FILENAME = "Top 5 Considerations Before Signing an Exclusive Agency Agreement.pdf"
ENCODED_FILENAME = quote(PDF_FILENAME)
PDF_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ENCODED_FILENAME}"

# Session state setup
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'captcha' not in st.session_state:
    st.session_state.captcha = {'num1': 0, 'num2': 0}

def display_logo():
    try:
        # Centered logo with controlled size
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image("Stirling_QR_Logo.png", width=150)  # Reduced width
    except Exception as e:
        st.error(f"Missing logo file: {str(e)}")
        st.stop()

def generate_captcha():
    st.session_state.captcha = {
        'num1': random.randint(1, 9),
        'num2': random.randint(1, 9)
    }

# Login management (keep existing login code)
# ... [keep the existing login code unchanged] ...

if st.session_state.logged_in:
    st.title("🔐 Leads Dashboard")
    try:
        leads_df = pd.read_csv("leads.csv")
        # ... [keep existing lead management code unchanged] ...
    except FileNotFoundError:
        st.warning("No leads collected yet")
    st.stop()

# Main Form
if not st.session_state.submitted:
    display_logo()
    
    st.title("Download Our Agency Agreement Guide")
    
    with st.form("lead_form", clear_on_submit=True):
        # Generate new CAPTCHA on form load
        if 'captcha' not in st.session_state:
            generate_captcha()
            
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone Number*")
        company = st.text_input("Company Name (optional)")
        
        # Simple CAPTCHA
        captcha_question = f"What is {st.session_state.captcha['num1']} + {st.session_state.captcha['num2']}?"
        captcha_answer = st.number_input(captcha_question, step=1, min_value=0)
        
        # Disclaimer text
        st.markdown("""
        <small><i>By clicking "Get Your Copy Now", you agree to Stirling Q&R contacting you 
        regarding this request. Your information will only be used for this purpose.</i></small>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Get Your Copy Now")
        
        if submitted:
            valid_captcha = (captcha_answer == st.session_state.captcha['num1'] + st.session_state.captcha['num2'])
            
            if all([name, email, phone]) and valid_captcha:
                new_lead = pd.DataFrame({
                    "Name": [name],
                    "Email": [email],
                    "Phone": [phone.replace(" ", "")],
                    "Company": [company],
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Contacted": False,
                    "Added to Vincere": False
                })
                
                try:
                    existing = pd.read_csv("leads.csv")
                    updated = pd.concat([existing, new_lead])
                except FileNotFoundError:
                    updated = new_lead
                
                updated.to_csv("leads.csv", index=False)
                st.session_state.submitted = True
                generate_captcha()  # Reset for next user
                st.rerun()
            else:
                if not valid_captcha:
                    st.error("Incorrect CAPTCHA answer - please try again")
                    generate_captcha()
                else:
                    st.error("Please complete all required fields")

# Success Page
else:
    display_logo()
    
    st.title("🎉 Your Guide is Ready!")
    
    # Auto-download
    st.markdown(f"""
    <a id="auto-dl" href="{PDF_URL}" download="{PDF_FILENAME}" hidden></a>
    <script>
        document.getElementById('auto-dl').click();
    </script>
    
    [Click here if download doesn't start]({PDF_URL})
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **What Happens Next:**
    
    - Expect contact from our team within 48 hours
    - Save our direct contact info:
      📧 talent@stirlingqr.com  
      📞 UK: +44 1293 307 201  
      📞 US: +1 415 808 5554
    
    *Contact us immediately for urgent requirements!*
    """)
