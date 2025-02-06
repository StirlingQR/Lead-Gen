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

# Color scheme
COLORS = {
    "primary": "#387E2E",
    "secondary": "#6BC651",
    "accent": "#4AA83E",
    "light": "#F0F0F0",
    "dark": "#0E1116",
    "white": "#FFFFFF"
}

# GitHub configuration
GITHUB_USER = "StirlingQR"
REPO_NAME = "Lead-Gen"
BRANCH = "main"
PDF_FILENAME = "Top 5 Considerations Before Signing an Exclusive Agency Agreement.pdf"
ENCODED_FILENAME = quote(PDF_FILENAME)
PDF_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ENCODED_FILENAME}"

# ==============
# SESSION STATE
# ==============
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'captcha' not in st.session_state:
    st.session_state.captcha = {'num1': 0, 'num2': 0}

# ==============
# CUSTOM STYLES
# ==============
st.markdown(f"""
<style>
    .stApp {{
        background-color: {COLORS['light']};
    }}
    .stHeader {{
        background-color: {COLORS['primary']} !important;
        color: {COLORS['white']} !important;
        padding: 1rem;
        border-radius: 8px;
    }}
    .stButton>button {{
        background-color: {COLORS['secondary']} !important;
        color: {COLORS['white']} !important;
        border-radius: 8px;
    }}
    .logo-container {{
        text-align: center;
        margin: 1rem 0;
    }}
    .logo-img {{
        width: 200px;
        border: 2px solid {COLORS['primary']};
        border-radius: 8px;
        padding: 5px;
    }}
</style>
""", unsafe_allow_html=True)

# ==============
# COMPONENTS
# ==============
def display_logo():
    try:
        st.markdown('<div class="logo-container"><img class="logo-img" src="https://raw.githubusercontent.com/StirlingQR/Lead-Gen/main/Stirling_QR_Logo.png"></div>', unsafe_allow_html=True)
    except:
        st.error("Logo loading issue - proceeding without logo")

def generate_captcha():
    st.session_state.captcha = {
        'num1': random.randint(1, 9),
        'num2': random.randint(1, 9)
    }

def check_duplicate(email, phone):
    try:
        existing = pd.read_csv("leads.csv")
        return existing[(existing['Email'] == email) | (existing['Phone'] == phone)].any().any()
    except FileNotFoundError:
        return False

# ==============
# LEAD MANAGEMENT
# ==============
if st.session_state.logged_in:
    st.title("🔐 Leads Dashboard")
    try:
        leads_df = pd.read_csv("leads.csv")
        
        # Add Contacted column if missing
        if 'Contacted' not in leads_df.columns:
            leads_df['Contacted'] = False
            
        # Status filtering
        status_filter = st.selectbox("Filter Leads", ['All', 'New', 'Contacted'])
        filtered_df = leads_df[leads_df['Contacted'] == (status_filter == 'Contacted')] if status_filter != 'All' else leads_df
        
        # Editable table
        edited_df = st.data_editor(
            filtered_df,
            column_config={
                "Contacted": st.column_config.CheckboxColumn(
                    "Contacted?",
                    help="Mark when lead has been contacted"
                )
            },
            use_container_width=True
        )
        
        if st.button("Save Changes"):
            leads_df.update(edited_df)
            leads_df.to_csv("leads.csv", index=False)
            st.success("Status updates saved!")
            
        if st.download_button("Export Leads", data=leads_df.to_csv(index=False), file_name="stirling_leads.csv"):
            st.success("Exported successfully")
            
    except FileNotFoundError:
        st.warning("No leads collected yet")
    st.stop()

# ==============
# MAIN FORM
# ==============
if not st.session_state.submitted:
    display_logo()
    
    with st.container():
        st.markdown(f'<div style="background-color:{COLORS["white"]};padding:2rem;border-radius:8px;">', unsafe_allow_html=True)
        st.title("Download Our Agency Agreement Guide")
        
        with st.form("lead_form", clear_on_submit=True):
            # Generate CAPTCHA
            if 'captcha' not in st.session_state:
                generate_captcha()
                
            name = st.text_input("Full Name*")
            email = st.text_input("Email*")
            phone = st.text_input("Phone Number*")
            company = st.text_input("Company Name (optional)")
            
            # CAPTCHA section
            st.markdown(f"""**CAPTCHA:** What is {st.session_state.captcha['num1']} + {st.session_state.captcha['num2']}?""")
            captcha_answer = st.number_input("Answer", step=1, min_value=0, key="captcha_input")
            
            # Agreement text
            st.markdown("""
            <small><i>By clicking below, you agree to Stirling Q&R contacting you</i></small>
            """, unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Get Your Copy Now →")
            
            if submitted:
                valid_captcha = (captcha_answer == st.session_state.captcha['num1'] + st.session_state.captcha['num2'])
                is_duplicate = check_duplicate(email, phone)
                
                if all([name, email, phone]) and valid_captcha and not is_duplicate:
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
                    generate_captcha()
                    st.rerun()
                else:
                    if not valid_captcha:
                        st.error("CAPTCHA verification failed")
                        generate_captcha()
                    elif is_duplicate:
                        st.error("This email or phone number already exists in our system")
                    else:
                        st.error("Please complete all required fields")
        st.markdown('</div>', unsafe_allow_html=True)

# ==============
# SUCCESS PAGE
# ==============
else:
    display_logo()
    st.markdown(f'<div style="background-color:{COLORS["white"]};padding:2rem;border-radius:8px;">', unsafe_allow_html=True)
    st.title("🎉 Your Guide is Ready!")
    
    # Auto-download
    st.markdown(f"""
    <a id="auto-dl" href="{PDF_URL}" download="{PDF_FILENAME}" hidden></a>
    <script>
        document.getElementById('auto-dl').click();
    </script>
    
    [Click here if download doesn't start]({PDF_URL})
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    **Next Steps:**
    
    - Expect contact from our team within 48 hours
    - Save our direct contact info:
      📧 talent@stirlingqr.com  
      📞 UK: +44 1293 307 201  
      📞 US: +1 415 808 5554
    
    *Contact us immediately for urgent requirements!*
    """)
    st.markdown('</div>', unsafe_allow_html=True)
