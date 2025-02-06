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
    "secondary": "#5B8C5A",  # Medium green
    "background": "#FFFFFF",  # White
    "text": "#333333",        # Dark gray
}

# GitHub configuration
GITHUB_USER = "StirlingQR"
REPO_NAME = "Lead-Gen"
BRANCH = "main"
PDF_FILENAME = "Top 5 Considerations Before Signing an Exclusive Agency Agreement.pdf"
ENCODED_FILENAME = quote(PDF_FILENAME)
PDF_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ENCODED_FILENAME}"
PRIVACY_URL = "https://www.stirlingqr.com/privacy"

# ==============
# SESSION STATE
# ==============
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'captcha' not in st.session_state:
    st.session_state.captcha = {'num1': random.randint(1,9), 'num2': random.randint(1,9)}

# ==============
# CUSTOM STYLES
# ==============
st.markdown(f"""
<style>
    .stApp {{
        background-color: {COLORS['background']};
    }}
    .logo-img {{
        width: 180px;
        display: block;
        margin: 0 auto 1.5rem;
    }}
    .consent-text {{
        font-size: 0.85rem;
        color: #666666;
        font-style: italic;
        margin: 1rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# ==============
# COMPONENTS
# ==============
def display_logo():
    try:
        st.markdown('<img class="logo-img" src="https://raw.githubusercontent.com/StirlingQR/Lead-Gen/main/Stirling_QR_Logo.png">', 
                   unsafe_allow_html=True)
    except:
        st.error("Logo loading issue")

def generate_captcha():
    st.session_state.captcha = {
        'num1': random.randint(1,9),
        'num2': random.randint(1,9)
    }

def check_duplicate(email, phone):
    try:
        existing = pd.read_csv("leads.csv")
        return existing[(existing['Email'].str.lower() == email.lower()) | 
                        (existing['Phone'] == phone)].any().any()
    except FileNotFoundError:
        return False

# ==============
# ADMIN SYSTEM
# ==============
# Persistent admin button
admin_col, _ = st.columns([1,5])
with admin_col:
    if st.session_state.logged_in:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        if st.button("Admin Login"):
            st.session_state.show_login = True

if 'show_login' in st.session_state and st.session_state.show_login:
    with st.form("Admin Login"):
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
        
        # Initialize Contacted column
        if 'Contacted' not in leads_df.columns:
            leads_df['Contacted'] = False
            
        # Filtering system
        status_filter = st.selectbox("Filter Leads", ['All', 'New', 'Contacted'])
        
        if status_filter == 'New':
            filtered_df = leads_df[~leads_df['Contacted']]
        elif status_filter == 'Contacted':
            filtered_df = leads_df[leads_df['Contacted']]
        else:
            filtered_df = leads_df

        # Editable table with delete buttons
        for index, row in filtered_df.iterrows():
            cols = st.columns([4,4,4,2,1])
            with cols[0]: st.write(row['Name'])
            with cols[1]: st.write(row['Email'])
            with cols[2]: st.write(row['Phone'])
            with cols[3]: 
                contacted = st.checkbox("Contacted", value=row['Contacted'], key=f"contacted_{index}")
                if contacted != row['Contacted']:
                    leads_df.at[index, 'Contacted'] = contacted
            with cols[4]: 
                if st.button("❌", key=f"del_{index}"):
                    leads_df = leads_df.drop(index)
            
        # Save changes
        if st.button("Save All Changes"):
            leads_df.to_csv("leads.csv", index=False)
            st.success("Changes saved!")
            
        # Export
        st.download_button("Export CSV", data=leads_df.to_csv(index=False), 
                         file_name="stirling_leads.csv")
            
    except FileNotFoundError:
        st.warning("No leads collected yet")
    st.stop()

# ==============
# MAIN FORM
# ==============
if not st.session_state.submitted:
    display_logo()
    st.title("Download Agency Agreement Guide")
    
    with st.form("lead_form", clear_on_submit=True):
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone Number*")
        company = st.text_input("Company Name (optional)")
        
        # CAPTCHA with random numbers
        st.markdown(f"**CAPTCHA:** What is {st.session_state.captcha['num1']} + {st.session_state.captcha['num2']}?")
        captcha_answer = st.number_input("Answer", step=1)
        
        # Consent text
        st.markdown(f"""
        <div class="consent-text">
            By submitting, you agree to Stirling Q&R contacting you. 
            View our <a href="{PRIVACY_URL}">privacy policy</a>.
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
                generate_captcha()  # Generate new CAPTCHA after submission
                st.session_state.submitted = True
                st.rerun()
            else:
                if not valid_captcha:
                    st.error("CAPTCHA verification failed")
                    generate_captcha()
                elif is_duplicate:
                    st.error("This contact information already exists")
                else:
                    st.error("Please complete all required fields")

# ==============
# SUCCESS PAGE
# ==============
else:
    display_logo()
    st.title("🎉 Your Guide is Ready!")
    
    st.markdown(f"""
    <a id="auto-dl" href="{PDF_URL}" download="{PDF_FILENAME}" hidden></a>
    <script>
        document.getElementById('auto-dl').click();
    </script>
    
    [Click here if download doesn't start]({PDF_URL})
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **Next Steps:**
    
    - Expect contact within 48 hours
    - Save our details:  
      📧 talent@stirlingqr.com  
      📞 UK: +44 1293 307 201  
      📞 US: +1 415 808 5554
    
    *Urgent needs? Contact us immediately!*
    """)
