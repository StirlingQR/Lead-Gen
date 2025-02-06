# pages/login.py
import streamlit as st

st.set_page_config(page_title="Admin Login", page_icon="🔐")

st.title("🔐 Admin Login")

with st.form("login"):
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    
    if st.form_submit_button("Login"):
        if user == "chris@stirlingqr.com" and pwd == "Measure897!":
            st.session_state.logged_in = True
            st.switch_page("app.py")
        else:
            st.error("Invalid credentials")
