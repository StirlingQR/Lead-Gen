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

# File paths with error handling
def validate_files():
    required_files = {
        "LOGO": Path(__file__).parent / "Stirling_QR_Logo.png",
        "PDF": Path(__file__.parent / "document.pdf"
    }
    
    missing = [name for name, path in required_files.items() if not path.exists()]
    if missing:
        st.error(f"Missing files: {', '.join(missing)}")
        st.stop()
    return required_files

files = validate_files()

# Initialize session states
session_defaults = {
    'submitted': False,
    'logged_in': False,
    'delete_leads': []
}
for key, val in session_defaults.items():
    st.session_state.setdefault(key, val)

# Logo display component
def display_logo():
    try:
        st.image(str(files["LOGO"]), use_container_width=True)
    except Exception as e:
        st.error(f"Logo display error: {str(e)}")
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
            leads_df = pd.read_csv("leads.csv")
            
            # Delete leads functionality
            with st.expander("Manage Leads"):
                for idx, row in leads_df.iterrows():
                    cols = st.columns([5,1])
                    cols[0].write(f"{row['Name']} - {row['Email']}")
                    if cols[1].button("Delete", key=f"del_{idx}"):
                        st.session_state.delete_leads.append(idx)
                
                if st.button("Confirm Deletions"):
                    leads_df = leads_df.drop(st.session_state.delete_leads)
                    leads_df.to_csv("leads.csv", index=False)
                    st.session_state.delete_leads = []
                    st.rerun()
            
            st.dataframe(leads_df, use_container_width=True)
            
            # CSV export
            csv = leads_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="leads.csv",
                mime="text/csv"
            )
            
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()
                
        except FileNotFoundError:
            st.warning("No leads collected yet")
        
        st.stop()

# Main form component
def lead_form():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("Download Our Quality Assurance Recruitment Guide")
    
    with st.form("lead_form"):
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone Number*")
        company = st.text_input("Company Name (optional)")
        
        st.markdown("""
        *By entering your information, you consent to Stirling Q&R collecting and storing your details. 
        You are opting in to be contacted by our team via email or phone to discuss your recruitment needs. 
        Your data will be handled securely and will not be shared with third parties without your consent.*
        """)
        
        if st.form_submit_button("Download Now →"):
            if all([name, email, phone]):
                new_lead = {
                    "Name": name,
                    "Email": email,
                    "Phone": phone,
                    "Company": company,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                try:
                    leads_df = pd.read_csv("leads.csv")
                    leads_df = pd.concat([leads_df, pd.DataFrame([new_lead])])
                except FileNotFoundError:
                    leads_df = pd.DataFrame([new_lead])
                
                leads_df.to_csv("leads.csv", index=False)
                st.session_state.submitted = True
                st.rerun()
            else:
                st.error("Please complete all required fields")

# Thank you page
def thank_you():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("🎉 Download Complete!")
    st.balloons()
    
    st.download_button(
        label="Download Guide (PDF)",
        data=files["PDF"].read_bytes(),
        file_name="QA_Recruitment_Guide.pdf",
        mime="application/octet-stream"
    )
    
    st.markdown("""
    **Your document should begin downloading automatically.**  
    If it doesn't start within a few seconds, click the download button above.
    
    ### Next Steps:
    1. Check your email for confirmation
    2. Expect our follow-up within 24 hours
    3. Save our contact: +44 1234 567890
    
    *Looking forward to helping with your QA recruitment needs!*
    """)

# App flow control
admin_panel()

if not st.session_state.submitted:
    lead_form()
else:
    thank_you()
