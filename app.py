# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote

# Configure page
st.set_page_config(
    page_title="Stirling Q&R - Exclusive Agency Guide",
    page_icon="📈",
    layout="centered"
)

# GitHub configuration
GITHUB_USER = "your-github-username"
REPO_NAME = "your-repo-name"
PDF_FILENAME = "Top 5 Considerations Before Signing an Exclusive Agency Agreement.pdf"

# Encode filename for URL
ENCODED_FILENAME = quote(PDF_FILENAME)
PDF_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/{ENCODED_FILENAME}"

def handle_download():
    """Trigger PDF download with proper filename"""
    st.markdown(
        f'<a href="{PDF_URL}" download="{PDF_FILENAME}" id="auto-download"></a>',
        unsafe_allow_html=True
    )
    st.write(
        """<script>document.getElementById('auto-download').click()</script>""",
        unsafe_allow_html=True
    )

# Session state management
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Lead capture form
if not st.session_state.submitted:
    st.title("Download 2025 Exclusive Agency Guide")
    
    with st.form("lead_form"):
        name = st.text_input("Full Name*")
        email = st.text_input("Work Email*")
        phone = st.text_input("Direct Phone*")
        company = st.text_input("Company Name (optional)")
        
        if st.form_submit_button("Get Your Guide →"):
            if all([name, email, phone]):
                # Save lead to CSV (existing code)
                st.session_state.submitted = True
                st.rerun()

# Download page
else:
    st.title("🎉 Your Guide is Ready!")
    st.balloons()
    
    # Automatic download attempt
    handle_download()
    
    # Fallback UI
    st.markdown(f"""
    **Didn't download automatically?**  
    [Click here to download]({PDF_URL})
    """)
    
    st.markdown("""
    **Next Steps:**
    1. Except contact from us within 48 hours
    2. [Book Strategy Session](https://calendly.com/stirlingqr)
    3. Save our number: UK: +44 1293 307201 | US: +1 415 808 5554
    """)
