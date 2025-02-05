# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Stirling Q&R - Exclusive Agency Guide",
    page_icon="📈",
    layout="centered"
)

# File paths (update with your actual GitHub raw URLs)
LOGO_PATH = Path(__file__).parent / "Stirling_QR_Logo.png"
PDF_URL = "https://raw.githubusercontent.com/[your-username]/[your-repo]/main/Top-5-Considerations-Before-Signing-an-Exclusive-Agency-Agreement.pdf"

# Initialize session states
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def display_logo():
    """Display logo with error handling"""
    try:
        st.image(str(LOGO_PATH), use_container_width=True)
    except Exception as e:
        st.error(f"Missing logo file: {LOGO_PATH.name}")
        st.stop()

# Admin panel with enhanced lead management
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
            
            # Enhanced lead management
            with st.expander("Manage Leads (Delete with 🗑️)"):
                for idx in reversed(range(len(leads_df))):
                    cols = st.columns([3,2,1,1])
                    cols[0].write(f"**{leads_df.iloc[idx]['Name']}**")
                    cols[1].write(f"{leads_df.iloc[idx]['Email']}")
                    cols[2].write(f"{leads_df.iloc[idx]['Phone']}")
                    if cols[3].button("🗑️", key=f"del_{idx}"):
                        leads_df = leads_df.drop(index=idx)
                        leads_df.to_csv("leads.csv", index=False)
                        st.rerun()
            
            # Real-time statistics
            st.markdown("### Placement Metrics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Leads", len(leads_df))
            col2.metric("Recent Submissions", leads_df[leads_df['Timestamp'] > pd.Timestamp.now() - pd.DateOffset(days=7)].shape[0])
            col3.metric("Companies", leads_df['Company'].nunique())
            
            st.download_button(
                "Download Full Lead Data", 
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

# Main lead capture form
def lead_form():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("Download 2025 Exclusive Agency Guide")
    
    with st.form("lead_form"):
        name = st.text_input("Full Name*")
        email = st.text_input("Work Email*")
        phone = st.text_input("Direct Phone*", help="Include country code")
        company = st.text_input("Company Name (optional)")
        
        st.markdown("""
        *By submitting, you agree to Stirling Q&R's Privacy Policy and consent to being contacted 
        about Quality/Regulatory recruitment solutions.*
        """)
        
        if st.form_submit_button("Get Your Guide →"):
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
            else:
                st.error("Please complete all required fields")

# PDF Viewer Page
def pdf_viewer():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("Your 2025 Exclusive Agency Guide")
    st.balloons()
    
    # PDF Viewer with Google Docs integration
    st.markdown(f"""
    <iframe src="https://docs.google.com/viewer?url={PDF_URL}&embedded=true" 
            width="100%" 
            height="800px" 
            style="border: none; margin-top: 20px;">
    </iframe>
    """, unsafe_allow_html=True)
    
    # Download options
    st.markdown(f"""
    <div style="margin-top: 30px; text-align: center;">
        <a href="{PDF_URL}" download>
            <button style="
                background-color: #0047AB;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;">
                📥 Download Full Guide
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **Next Steps:**
    1. Review key considerations (hyperlinks work in downloaded PDF)
    2. [Book Strategy Session](https://calendly.com/stirlingqr)
    3. Contact Chris: +44 1234 567890
    """)

# App flow control
admin_panel()

if not st.session_state.submitted:
    lead_form()
else:
    pdf_viewer()
