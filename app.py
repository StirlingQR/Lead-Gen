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
    "primary": "#2C5F2D",    # Dark green
    "secondary": "#97BC62",  # Sage green
    "background": "#FFFFFF",  # White
    "text": "#2C2C2C",       # Dark gray
    "border": "#E0E0E0"      # Light gray
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
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# ==============
# CUSTOM STYLES
# ==============
st.markdown(f"""
<style>
    .stApp {{
        background-color: {COLORS['background']};
    }}
    .main-container {{
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        background-color: {COLORS['background']};
    }}
    h1 {{
        color: {COLORS['primary']} !important;
        margin-bottom: 1.5rem;
    }}
    .stButton>button {{
        background-color: {COLORS['primary']} !important;
        color: {COLORS['background']} !important;
        border-radius: 8px;
        font-weight: 500;
    }}
    .stButton>button:hover {{
        background-color: {COLORS['secondary']} !important;
    }}
    .logo-img {{
        height: 80px;
        display: block;
        margin: 0 auto;
    }}
    .consent-text {{
        font-size: 0.9rem;
        color: #666666;
        margin: 1.5rem 0;
        padding: 1rem;
        background-color: #F8F8F8;
        border-radius: 8px;
    }}
</style>
""", unsafe_allow_html=True)

# ==============
# COMPONENTS
# ==============
def display_logo():
    try:
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <img class="logo-img" src="https://raw.githubusercontent.com/StirlingQR/Lead-Gen/main/Stirling_QR_Logo.png">
        </div>
        """, unsafe_allow_html=True)
    except:
        st.error("Error loading logo")

def generate_captcha():
    st.session_state.captcha = {
        'num1': random.randint(1, 9),
        'num2': random.randint(1, 9)
    }

def check_duplicate(email, phone):
    try:
        existing = pd.read_csv("leads.csv")
        return existing[(existing['Email'].str.lower() == email.lower()) | 
                        (existing['Phone'] == phone)].any().any()
    except FileNotFoundError:
        return False

# ==============
# ADMIN LOGIN
# ==============
# Login button at top left
login_col, _ = st.columns([1, 5])
with login_col:
    if not st.session_state.logged_in:
        if st.button("Admin Login"):
            st.session_state.show_login = True
    else:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.show_login = False
            st.rerun()

# Login form in main content area
if st.session_state.show_login and not st.session_state.logged_in:
    with st.form("Login"):
        st.subheader("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Authenticate"):
            if username == "chris@stirlingqr.com" and password == "Measure897!":
                st.session_state.logged_in = True
                st.session_state.show_login = False
                st.rerun()
            else:
                st.error("Invalid credentials")

# ==============
# LEAD MANAGEMENT
# ==============
if st.session_state.logged_in:
    st.title("🔐 Leads Dashboard")
    try:
        leads_df = pd.read_csv("leads.csv")
        
        if 'Contacted' not in leads_df.columns:
            leads_df['Contacted'] = False
            
        status_filter = st.selectbox("Filter Leads", ['All', 'New', 'Contacted'])
        filtered_df = leads_df if status_filter == 'All' else \
                      leads_df[leads_df['Contacted'] == (status_filter == 'Contacted')]
        
        edited_df = st.data_editor(
            filtered_df,
            column_config={
                "Contacted": st.column_config.CheckboxColumn(
                    "Contacted?",
                    help="Mark when lead has been contacted",
                    default=False
                )
            },
            use_container_width=True,
            key="editor"
        )
        
        if st.button("Save Changes"):
            leads_df.update(edited_df)
            leads_df.to_csv("leads.csv", index=False)
            st.success("Status updates saved!")
            
        if st.download_button("Export Leads", data=leads_df.to_csv(index=False), 
                            file_name="stirling_leads.csv"):
            st.success("Exported successfully")
            
    except FileNotFoundError:
        st.warning("No leads collected yet")
    st.stop()

# ==============
# MAIN FORM
# ==============
if not st.session_state.submitted:
    with st.container():
        display_logo()
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        st.title("Download Agency Agreement Guide")
        
        with st.form("lead_form", clear_on_submit=True):
            if 'captcha' not in st.session_state:
                generate_captcha()
                
            name = st.text_input("Full Name*")
            email = st.text_input("Email*")
            phone = st.text_input("Phone Number*")
            company = st.text_input("Company Name (optional)")
            
            st.markdown(f"""
            **CAPTCHA Verification**  
            What is {st.session_state.captcha['num1']} + {st.session_state.captcha['num2']}?
            """)
            captcha_answer = st.number_input("Enter answer", step=1, min_value=0)
            
            st.markdown("""
            <div class="consent-text">
                <p>By submitting this form, you confirm that:</p>
                <ul>
                    <li>You are authorized to provide this information</li>
                    <li>Stirling Q&R may contact you using the details provided</li>
                    <li>Your data will be stored securely in our systems</li>
                    <li>You can request data deletion by emailing talent@stirlingqr.com</li>
                </ul>
            </div>
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
                        st.error("This contact information already exists in our system")
                    else:
                        st.error("Please complete all required fields")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==============
# SUCCESS PAGE
# ==============
else:
    with st.container():
        display_logo()
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        st.title("🎉 Your Guide is Ready!")
        
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
        
        *Urgent requirements? Contact us immediately!*
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
