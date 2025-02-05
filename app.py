# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Stirling Q&R Lead Generation",
    page_icon="📈",
    layout="centered"
)

# SharePoint PDF URL (replace with your actual link)
SHAREPOINT_PDF_URL = "https://davidsongray-my.sharepoint.com/:b:/g/personal/chris_stirling_stirlingqr_com/Ecck3wvpY9ZFngLCjJP4ECsBGmyh0PN1-m-GTGPzhIuhMg?e=d77jE6"

# Initialize paths with correct filename (no spaces)
LOGO_PATH = Path(__file__).parent / "Stirling_QR_Logo.png"

def display_logo():
    """Display logo with error handling"""
    try:
        st.image(str(LOGO_PATH), use_container_width=True)
    except Exception as e:
        st.error(f"Missing logo file: {LOGO_PATH.name}")
        st.stop()

# Login management
def admin_panel():
    with st.sidebar:
        if not st.session_state.logged_in:
            st.title("Admin Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                if username == "chris@stirlingqr.com" and password == "Measure897!":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    if st.session_state.logged_in:
        st.title("🔐 Leads Dashboard")
        
        try:
            leads_df = pd.read_csv("leads.csv", dtype={'Phone': str})
            
            # Delete leads interface
            st.write("**Manage Leads:**")
            for idx in reversed(range(len(leads_df))):
                cols = st.columns([4,1,1])
                cols[0].write(f"{leads_df.iloc[idx]['Name']} - {leads_df.iloc[idx]['Email']}")
                cols[1].write(leads_df.iloc[idx]['Phone'])
                if cols[2].button("🗑️", key=f"del_{idx}"):
                    leads_df = leads_df.drop(index=idx)
                    leads_df.to_csv("leads.csv", index=False)
                    st.rerun()
            
            st.download_button(
                "Download CSV", 
                leads_df.to_csv(index=False), 
                "leads.csv", 
                "text/csv"
            )
            
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()
                
        except FileNotFoundError:
            st.warning("No leads collected yet")
        st.stop()

def lead_form():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("Download Our Recruitment Guide")
    
    with st.form("lead_form"):
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone Number*", help="Enter as text to preserve formatting")
        company = st.text_input("Company Name (optional)")
        
        st.markdown("""*By entering your information...*""")  # Your privacy text
        
        if st.form_submit_button("Download Now →"):
            if all([name, email, phone]):
                new_lead = pd.DataFrame([{
                    "Name": name,
                    "Email": email,
                    "Phone": str(phone),
                    "Company": company,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                
                try:
                    existing = pd.read_csv("leads.csv", dtype={'Phone': str})
                    updated = pd.concat([existing, new_lead])
                except FileNotFoundError:
                    updated = new_lead
                
                updated.to_csv("leads.csv", index=False)
                st.session_state.submitted = True
                st.rerun()

def thank_you():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("🎉 Download Complete!")
    st.balloons()
    
    # SharePoint PDF download solution
    st.markdown(f"""
    <script>
    window.open("{SHAREPOINT_PDF_URL}", "_blank");
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    **Your download should start automatically.**  
    If not, [click here to download the guide]({SHAREPOINT_PDF_URL})
    """, unsafe_allow_html=True)

# App flow
admin_panel()
if not st.session_state.submitted:
    lead_form()
else:
    thank_you()
