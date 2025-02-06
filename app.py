# Success Page
else:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("🎉 Your Guide is Ready!")
    st.success("✅ Your download should start automatically!")

    # Auto-download and preview
    st.markdown(f"""
    <a id="auto-dl" href="{PDF_URL}" download hidden></a>
    <script>
        document.getElementById('auto-dl').click();
    </script>
    <iframe src="https://docs.google.com/viewer?url={PDF_URL}&embedded=true" 
            width="100%" 
            height="600" 
            style="border:none; margin-top: 1rem; margin-bottom: 2rem">
    </iframe>
    """, unsafe_allow_html=True)

    # What happens next section
    st.markdown("""
    **What Happens Next?**

    1. Our team will review your request
    2. You'll receive a confirmation within 24 hours
    3. We'll follow up to discuss your agency agreement needs

    *Need immediate assistance?*  
    📞 Call: +44 (0)1234 567890  
    📧 Email: chris@stirlingqr.com
    """)

    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    """, unsafe_allow_html=True)
