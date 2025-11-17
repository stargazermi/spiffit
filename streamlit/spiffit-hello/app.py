"""
Simple Streamlit Hello World App
For testing Databricks App deployment
"""

import streamlit as st
import datetime

# Page configuration
st.set_page_config(
    page_title="Hello World - Databricks App",
    page_icon="👋",
    layout="wide"
)

# Main content
st.title("👋 Hello World!")
st.markdown("---")

st.header("Welcome to Your First Databricks Streamlit App!")

st.write("""
This is a simple hello world app to test your Databricks App deployment.
If you can see this, your setup is working correctly! 🎉
""")

# Interactive elements
st.subheader("Interactive Demo")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("What's your name?", placeholder="Enter your name here")
    if name:
        st.success(f"Hello, {name}! 👋")

with col2:
    favorite_color = st.selectbox(
        "What's your favorite color?",
        ["Red", "Blue", "Green", "Yellow", "Purple"]
    )
    st.info(f"Great choice! {favorite_color} is awesome! 🎨")

# Display some info
st.markdown("---")
st.subheader("System Info")

col3, col4, col5 = st.columns(3)

with col3:
    st.metric("Current Time", datetime.datetime.now().strftime("%H:%M:%S"))

with col4:
    st.metric("Status", "✅ Running")

with col5:
    st.metric("Port", "8000")

# Sample button
st.markdown("---")
if st.button("Click me! 🚀"):
    st.balloons()
    st.success("Button clicked! You're ready to build something amazing!")

# Footer
st.markdown("---")
st.caption("Built with Streamlit for Databricks | Ready for your hackathon! 🎉")

