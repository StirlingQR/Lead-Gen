# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote
import smtplib
from email.message import EmailMessage

# Configure page
st.set_page_config(
    page_title="Stirling Q&R Lead Management",
    page_icon="📈",
    layout="wide"
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

def display_logo():
    try:
        st.image("Stirling_QR_Logo.png", use_container_width=True)
    except Exception as e:
        st.error(f"Missing logo file: {str(e)}")
        st.stop()

def send_notification(name, email):
    """Send email alert using Microsoft SMTP"""
    msg = EmailMessage()
    msg.set_content(f"New lead captured:\nName: {name}\nEmail: {email}")
    msg['Subject'] = '🚨 NEW LEAD - Stirling Q&R'
    msg['From'] = 'chris@stirlingqr.com'  # Use your Microsoft email
    msg['To'] = 'chris@stirlingqr.com'    # Receiver email
    
    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server: 
            server.starttls()
            server.login('chris@stirlingqr.com', 'your-password')  # Microsoft email password
            server.send_message(msg)
    except Exception as e:
        st.error(f"Error sending notification: {str(e)}")

# Login management
if not st.session_state.logged_in:
    if st.button("Admin Login", key="admin_login"):
        st.session_state.show_login = True
else:
    if st.button("Logout"):
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
            else:
                st.error("Invalid credentials")

if st.session_state.logged_in:
    st.title("🔐 Leads Dashboard")
    try:
        leads_df = pd.read_csv("leads.csv")
        
        # Add status columns if not exists
        for col in ['Contacted', 'Added to Vincere']:
            if col not in leads_df.columns:
                leads_df[col] = False
                
        # Status filtering
        status_filter = st.selectbox("Filter Leads", ['All', 'New', 'Contacted', 'Converted'])
        
        if status_filter == 'New':
            filtered_df = leads_df[~leads_df['Contacted']]
        elif status_filter == 'Contacted':
            filtered_df = leads_df[leads_df['Contacted']]
        elif status_filter == 'Converted':
            filtered_df = leads_df[leads_df['Added to Vincere']]
        else:
            filtered_df = leads_df

        # Editable status tracking
        edited_df = st.data_editor(
            filtered_df,
            column_config={
                "Contacted": st.column_config.CheckboxColumn(
                    "Contacted?",
                    help="Mark when lead has been contacted"
                ),
                "Added to Vincere": st.column_config.CheckboxColumn(
                    "In Vincere?",
                    help="Mark when lead is added to Vincere"
                )
            },
            use_container_width=True,
            key="lead_editor"
        )
        
        # Save status changes
        if st.button("Save Changes"):
            leads_df.update(edited_df)
            leads_df.to_csv("leads.csv", index=False)
            st.success("Status updates saved!")
            
        # Export button
        if st.download_button(
            label="Export All Leads",
            data=leads_df.to_csv(index=False),
            file_name="stirling_leads.csv",
            mime="text/csv"
        ):
            st.success("Exported successfully")
            
    except FileNotFoundError:
        st.warning("No leads collected yet")
    st.stop()

# Main Form
if not st.session_state.submitted:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("Download Our Agency Agreement Guide")
    
    with st.form("lead_form", clear_on_submit=True):
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone Number*")
        company = st.text_input("Company Name (optional)")
        
        submitted = st.form_submit_button("Get Your Copy Now")
        
        if submitted:
            if all([name, email, phone]):
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
                send_notification(name, email)
                st.session_state.submitted = True
                st.rerun()
            else:
                st.error("Please complete required fields")

# Success Page
else:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("🎉 Your Guide is Ready!")
    
    # Download system
    st.markdown(f"""
    <a id="auto-dl" href="{PDF_URL}" download="{PDF_FILENAME}" hidden></a>
    <script>
        document.getElementById('auto-dl').click();
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    [Download Now]({PDF_URL})
    """)
    
    st.markdown("""
    **Next Steps:**
    - Your download should start automatically
    - We'll review your request within 24 hours
    - Check your email for confirmation
    """)
