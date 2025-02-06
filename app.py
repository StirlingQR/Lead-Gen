# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote
import smtplib
from email.message import EmailMessage

# Configure page
st.set_page_config(
    page_title="Stirling Q&R Lead Generation",
    page_icon="📈",
    layout="centered"
)

# GitHub configuration - REPLACE WITH YOUR DETAILS
GITHUB_USER = "stirlington"
REPO_NAME = "Lead-Gen"
BRANCH = "main"
PDF_FILENAME = "Top 5 Considerations Before Signing an Exclusive Agency Agreement.pdf"

# Encoded PDF URL
ENCODED_FILENAME = quote(PDF_FILENAME)
PDF_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ENCODED_FILENAME}"

# Session state management
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def display_logo():
    """Display logo with error handling"""
    try:
        st.image("Stirling_QR_Logo.png", use_container_width=True)
    except Exception as e:
        st.error(f"Missing logo file: {str(e)}")
        st.stop()

def send_notification(name, email):
    """Send email alert for new lead"""
    msg = EmailMessage()
    msg.set_content(f"New lead received:\nName: {name}\nEmail: {email}")
    msg['Subject'] = '🚨 New Lead Alert!'
    msg['From'] = 'alerts@stirlingqr.com'  # Replace with your email
    msg['To'] = 'chris@stirlingqr.com'     # Replace with your email
    
    try:
        with smtplib.SMTP('your-smtp-server.com', 587) as server:  # Replace with your SMTP
            server.starttls()
            server.login('your@email.com', 'your-password')  # Replace with credentials
            server.send_message(msg)
    except Exception as e:
        st.error(f"Error sending notification: {str(e)}")

# Login button
if not st.session_state.logged_in:
    cols = st.columns([4,1])
    with cols[1]:
        if st.button("Admin Login"):
            st.switch_page("pages/login.py")

if st.session_state.logged_in:
    st.title("🔐 Leads Dashboard")
    
    try:
        leads_df = pd.read_csv("leads.csv")
        st.dataframe(
            leads_df.style.format({"Phone": lambda x: f"{x:.0f}"}),
            use_container_width=True
        )
        
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

if not st.session_state.submitted:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("Download Our Exclusive Agency Agreement Guide")
    
    with st.form("lead_form"):
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone Number*")
        company = st.text_input("Company Name (optional)")
        
        st.markdown("""*By entering your information...*""")  # Your privacy text
        
        if st.form_submit_button("Download Now →"):
            if all([name, email, phone]):
                new_lead = pd.DataFrame({
                    "Name": [name],
                    "Email": [email],
                    "Phone": [phone],
                    "Company": [company],
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                try:
                    existing = pd.read_csv("leads.csv")
                    updated = pd.concat([existing, new_lead])
                except FileNotFoundError:
                    updated = new_lead
                
                updated.to_csv("leads.csv", index=False)
                send_notification(name, email)
                st.session_state.submitted = True
                st.rerun()

else:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("🎉 Your Guide is Ready!")
    st.success("✅ Guide successfully downloaded! Check your email", icon="✅")
    st.toast('New lead captured!', icon='👤')
    
    # Auto-download and preview
    st.markdown(f"""
    <a id="auto-download" href="{PDF_URL}" download hidden></a>
    <script>
        document.getElementById('auto-download').click();
    </script>
    <iframe src="https://docs.google.com/viewer?url={PDF_URL}&embedded=true" 
            width="100%" 
            height="800px" 
            style="border: none; margin-top: 20px;">
    </iframe>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    """, unsafe_allow_html=True)
