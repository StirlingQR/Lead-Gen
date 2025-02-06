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
    """Send email alert for new lead"""
    msg = EmailMessage()
    msg.set_content(f"New lead received:\nName: {name}\nEmail: {email}")
    msg['Subject'] = '🚨 NEW LEAD - Stirling Q&R'
    msg['From'] = 'talent@stirlingqr.com'  
    msg['To'] = 'chris@stirlingqr.com'    
    
    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server: 
            server.starttls()
            server.login('chris.stirling@stirlingqr.com', 'Measure897!')
            server.send_message(msg)
            st.success("Notification sent successfully!")
    except Exception as e:
        st.error(f"Error sending notification: {str(e)}")
        raise  # Add this to see full error in logs

# Login management and other code remains the same...

# Success Page
else:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("🎉 Your Guide is Ready!")
    
    # Improved auto-download with multiple fallbacks
    st.markdown(f"""
    <a id="auto-download" href="{PDF_URL}" download hidden></a>
    <script>
        function triggerDownload() {{
            const link = document.getElementById('auto-download');
            link.click();
            setTimeout(() => {{ window.location.href = '{PDF_URL}'; }}, 1000);
        }}
        window.addEventListener('load', triggerDownload);
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <iframe src="https://docs.google.com/viewer?url={PDF_URL}&embedded=true" 
            width="100%" 
            height="600" 
            style="border:none; margin-top: 1rem; margin-bottom: 2rem">
    </iframe>
    """, unsafe_allow_html=True)
    
    # Updated next steps
    st.markdown("""
    **What Happens Next?**

    - Expect contact from one of our team within 48 hours
    - Save our details:  
      📧 talent@stirlingqr.com  
      📞 UK: +44 1293 307 201  
      📞 US: +1 415 808 5554  
      
    *Contact us immediately for urgent requirements!*
    """)
