import streamlit as st
import bcrypt

from utils.database import add_user, get_user

from dashboard import show_dashboard
from prediction import show_prediction_page
from history import show_history_page
from doctor import show_doctor_page
from profile_page import show_profile_page
from report import show_report_page
# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="Heart Disease Prediction System",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# Load CSS
# ======================================================

def load_css():
    try:
        with open("style.css", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()
# ======================================================
# Session State
# ======================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "menu" not in st.session_state:
    st.session_state.menu = "🔐 Login"
# =========================
# Sidebar
# =========================

st.sidebar.image(
    "https://img.icons8.com/color/96/heart-with-pulse.png",
    width=90
)

st.sidebar.markdown("""
# ❤️ Heart Disease
AI Prediction System
""")

# -----------------------
# BEFORE LOGIN
# -----------------------
if not st.session_state.logged_in:

    if "menu" not in st.session_state:
        st.session_state.menu = "🔐 Login"

    st.sidebar.markdown("### Navigation")

    if st.sidebar.button("🔐 Login", use_container_width=True):
        st.session_state.menu = "🔐 Login"

    if st.sidebar.button("📝 Register", use_container_width=True):
        st.session_state.menu = "📝 Register"

    menu = st.session_state.menu

# -----------------------
# AFTER LOGIN
# -----------------------
else:

    st.sidebar.markdown("### Navigation")

    pages = [
        "🏠 Dashboard",
        "❤️ Prediction",
        "📊 Analytics",
        "📜 History",
        "🩺 Doctors",
        "👤 Profile",
        "📄 Reports",
        "🚪 Logout"
    ]

    for page in pages:
        if st.sidebar.button(page, use_container_width=True):
            st.session_state.menu = page
            st.rerun()

    menu = st.session_state.menu
# ======================================================
# LOGIN
# ======================================================

if menu == "🔐 Login":

    col1, col2 = st.columns([1.2, 1])

    with col1:

        st.image(
            "https://img.icons8.com/color/512/heart-with-pulse.png",
            width=280
        )

        st.markdown("""
        <h1 style="color:#0F4C81;">Heart Disease Prediction</h1>
        <h3 style="color:#16A085;">AI Powered Healthcare System</h3>

        Predict heart disease risk using Machine Learning.

        ✔ Secure Login

        ✔ AI Prediction

        ✔ Dashboard Analytics

        ✔ PDF Reports
        """, unsafe_allow_html=True)

    with col2:

        st.subheader("🔐 Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login", use_container_width=True):

            user = get_user(username)

            if user and bcrypt.checkpw(
                password.encode(),
                user[3].encode()
            ):

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.menu = "🏠 Dashboard"

                st.rerun()

            else:
                st.error("Invalid Username or Password")

# ======================================================
# REGISTER
# ======================================================

elif menu == "📝 Register":

    st.title("📝 Create Account")

    username = st.text_input("Username")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register", use_container_width=True):

        if password != confirm:

            st.error("Passwords do not match.")

        else:

            hashed = bcrypt.hashpw(
                password.encode(),
                bcrypt.gensalt()
            ).decode()

            try:

                add_user(
                    username,
                    email,
                    hashed
                )

                st.success("Registration Successful")

                st.session_state.menu = "🔐 Login"

                st.rerun()

            except:

                st.error("Username already exists.")

# ======================================================
# DASHBOARD
# ======================================================

elif menu == "🏠 Dashboard":

    st.title(f"🏠 Welcome {st.session_state.username}")

    st.subheader("Quick Access")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if st.button("❤️ Prediction", use_container_width=True):
            st.session_state.menu = "❤️ Prediction"
            st.rerun()

    with c2:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.menu = "📊 Analytics"
            st.rerun()

    with c3:
        if st.button("📜 History", use_container_width=True):
            st.session_state.menu = "📜 History"
            st.rerun()

    with c4:
        if st.button("🩺 Doctors", use_container_width=True):
            st.session_state.menu = "🩺 Doctors"
            st.rerun()

    st.divider()

    left, right = st.columns([2,1])

    with left:

        st.info("""
### About Project

This application predicts heart disease using Machine Learning.

✔ Heart Disease Prediction

✔ Prediction History

✔ Dashboard Analytics

✔ Doctor Recommendation

✔ PDF Reports
""")

    with right:

        st.success("""
### ❤️ Health Tips

• Exercise 30 minutes

• Eat Healthy Food

• Drink Water

• Reduce Salt

• Check Blood Pressure
""")
        
elif menu == "❤️ Prediction":
    show_prediction_page()

elif menu == "📊 Analytics":
    show_dashboard()

elif menu == "📜 History":
    show_history_page()

elif menu == "🩺 Doctors":
    show_doctor_page()

elif menu == "👤 Profile":
    show_profile_page()

elif menu == "📄 Reports":
    show_report_page()

elif menu == "🚪 Logout":

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.menu = "🔐 Login"

    st.rerun()