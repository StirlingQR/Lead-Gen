# Replace the existing form section with this
with st.form("lead_form", clear_on_submit=True):
    name = st.text_input("Full Name*")
    email = st.text_input("Email*")
    phone = st.text_input("Phone Number*")
    company = st.text_input("Company Name (optional)")
    
    st.markdown("""*By entering your information...*""")
    
    # Changed to proper form submission handling
    submitted = st.form_submit_button("Download Now →")
    
if submitted:  # Moved outside the form context
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
