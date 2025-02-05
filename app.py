# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(page_title="Stirling Q&R Lead Generation", page_icon="📈")

# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Login management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login sidebar
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

# Admin panel
if st.session_state.logged_in:
    st.title("Leads Dashboard")
    try:
        leads_df = pd.read_csv("leads.csv")
        st.dataframe(leads_df)
        
        if st.download_button("Download CSV", data=leads_df.to_csv(), file_name="leads.csv", mime="text/csv"):
            st.success("CSV downloaded successfully")
            
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
            
    except FileNotFoundError:
        st.warning("No leads collected yet")
        
    return

# Main form
if not st.session_state.submitted:
    st.image("Stirling QR Logo.png", width=200)
    st.title("Download Our Exclusive Guide")
    
    with st.form("lead_form"):
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone Number*")
        
        st.markdown("_By entering your information, you consent to Stirling Q&R collecting and storing your details. You are opting in to be contacted by our team via email or phone to discuss your recruitment needs and how we can assist you. Your data will be handled securely and will not be shared with third parties without your consent. For more information, please review our Privacy Policy._")
        
        if st.form_submit_button("Download Now"):
            if name and email and phone:
                # Save lead
                new_lead = pd.DataFrame([[name, email, phone, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                                       columns=["Name", "Email", "Phone", "Timestamp"])
                
                try:
                    existing_leads = pd.read_csv("leads.csv")
                    updated_leads = pd.concat([existing_leads, new_lead], ignore_index=True)
                except FileNotFoundError:
                    updated_leads = new_lead
                    
                updated_leads.to_csv("leads.csv", index=False)
                
                # Trigger download
                with open("document.pdf", "rb") as f:
                    st.download_button("Click here if download doesn't start automatically",
                                      data=f,
                                      file_name="QA_Recruitment_Guide.pdf",
                                      mime="application/pdf")
                
                st.session_state.submitted = True
                st.rerun()
            else:
                st.error("Please fill all mandatory fields")

# Thank you page
else:
    st.image("Stirling QR Logo.png", width=200)
    st.title("Thank You for Downloading!")
    st.markdown("""
    Your document should begin downloading automatically. 
    If it doesn't start within a few seconds, click the download button above.
    
    **Next Steps:**
    - Check your email for a confirmation
   - Expect a follow-up call from our team within 24 hours
    - Save our number: UK: +44 1293 307201 | US: +1 415 808 5554
    """)
