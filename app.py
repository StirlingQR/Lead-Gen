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
    st.session_state.captcha = {'num1': random.randint(1,9), 'num2': random.randint(1,9)}
if 'leads_df' not in st.session_state:
    st.session_state.leads_df = pd.DataFrame()

def display_logo():
    try:
        st.image("Stirling_QR_Logo.png", use_container_width=True, width=150)
    except:
        st.error("Logo loading issue")

# Login management
if not st.session_state.logged_in:
    if st.sidebar.button("Admin Login"):
        st.session_state.show_login = True
else:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.show_login = False
        st.rerun()

if 'show_login' in st.session_state and st.session_state.show_login:
    with st.form("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Authenticate"):
            if username == "chris@stirlingqr.com" and password == "Measure897!":
                st.session_state.logged_in = True
                st.session_state.show_login = False
                st.rerun()

if st.session_state.logged_in:
    st.title("🔐 Leads Dashboard")
    try:
        st.session_state.leads_df = pd.read_csv("leads.csv")
        
        # Delete functionality
        st.markdown("### Current Leads")
        for index, row in st.session_state.leads_df.iterrows():
            cols = st.columns([5,4,4,2,1])
            with cols[0]: st.write(row['Name'])
            with cols[1]: st.write(row['Email'])
            with cols[2]: st.write(row['Phone'])
            with cols[3]: 
                contacted = st.checkbox("Contacted", value=row.get('Contacted', False), 
                                      key=f"contacted_{index}")
                if contacted != row.get('Contacted', False):
                    st.session_state.leads_df.at[index, 'Contacted'] = contacted
            with cols[4]: 
                if st.button("❌", key=f"del_{index}"):
                    st.session_state.leads_df = st.session_state.leads_df.drop(index)
                    st.session_state.leads_df.to_csv("leads.csv", index=False)
                    st.experimental_rerun()
        
        # Save changes
        if st.button("Save All Changes"):
            st.session_state.leads_df.to_csv("leads.csv", index=False)
            st.success("Changes saved!")
            
    except FileNotFoundError:
        st.warning("No leads collected yet")
    st.stop()

# Main Form
if not st.session_state.submitted:
    display_logo()
    st.title("Download Agency Agreement Guide")
    
    with st.form("lead_form", clear_on_submit=True):
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone Number*")
        company = st.text_input("Company Name (optional)")
        
        # CAPTCHA
        st.markdown(f"**CAPTCHA:** What is {st.session_state.captcha['num1']} + {st.session_state.captcha['num2']}?")
        captcha_answer = st.number_input("Answer", step=1)
        
        submitted = st.form_submit_button("Get Your Copy Now →")
        
        if submitted:
            valid_captcha = (captcha_answer == st.session_state.captcha['num1'] + st.session_state.captcha['num2'])
            if valid_captcha:
                new_lead = pd.DataFrame({
                    "Name": [name],
                    "Email": [email],
                    "Phone": [phone.replace(" ", "")],
                    "Company": [company],
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Contacted": False
                })
                
                try:
                    existing = pd.read_csv("leads.csv")
                    updated = pd.concat([existing, new_lead])
                except FileNotFoundError:
                    updated = new_lead
                
                updated.to_csv("leads.csv", index=False)
                st.session_state.submitted = True
                st.session_state.captcha = {'num1': random.randint(1,9), 'num2': random.randint(1,9)}
                st.experimental_rerun()

# Success Page
else:
    display_logo()
    st.title("🎉 Your Guide is Ready!")
    
    # Download section
    st.markdown(f"""
    <a id="auto-dl" href="{PDF_URL}" download="{PDF_FILENAME}" hidden></a>
    <script>
        document.getElementById('auto-dl').click();
    </script>
    """, unsafe_allow_html=True)
    
    st.download_button(
        label="Download Guide Now",
        data=requests.get(PDF_URL).content,
        file_name=PDF_FILENAME,
        mime="application/pdf"
    )
    
    st.markdown("""
    **Next Steps:**
    - Expect contact within 48 hours
    - Save our details:  
      📧 talent@stirlingqr.com  
      📞 UK: +44 1293 307 201  
      📞 US: +1 415 808 5554
    """)
