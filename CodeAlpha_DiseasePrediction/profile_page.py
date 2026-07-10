import streamlit as st

def show_profile_page():

    st.title("👤 User Profile")

    st.write("### Username")
    st.success(st.session_state.username)

    st.write("### Email")
    st.info("user@example.com")

    st.write("### Account Status")
    st.success("Active")

    st.write("### Project")
    st.write("Heart Disease Prediction System")