import streamlit as st
import joblib
import numpy as np

from utils.database import save_prediction
from report import generate_report

# Load model
model = joblib.load("heart_model.pkl")


def show_prediction_page():

    st.markdown("""
    <h1 class='main-title'>
    ❤️ Heart Disease Prediction
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("👤 Patient Information")

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input("Age", 1, 120, 30)

        sex = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        cp = st.selectbox(
            "Chest Pain Type",
            [0, 1, 2, 3]
        )

        trestbps = st.number_input(
            "Resting Blood Pressure",
            80, 250, 120
        )

        chol = st.number_input(
            "Cholesterol",
            100, 600, 200
        )

        fbs = st.selectbox(
            "Fasting Blood Sugar",
            [0, 1]
        )

        restecg = st.selectbox(
            "Rest ECG",
            [0, 1, 2]
        )

    with col2:

        thalach = st.number_input(
            "Maximum Heart Rate",
            60, 220, 150
        )

        exang = st.selectbox(
            "Exercise Induced Angina",
            [0, 1]
        )

        oldpeak = st.number_input(
            "Old Peak",
            0.0,
            10.0,
            1.0
        )

        slope = st.selectbox(
            "Slope",
            [0, 1, 2]
        )

        ca = st.selectbox(
            "Major Vessels",
            [0, 1, 2, 3, 4]
        )

        thal = st.selectbox(
            "Thal",
            [0, 1, 2, 3]
        )

    sex = 1 if sex == "Male" else 0

    st.write("")

    if st.button("❤️ Predict Heart Disease", use_container_width=True):

        features = np.array([[
            age,
            sex,
            cp,
            trestbps,
            chol,
            fbs,
            restecg,
            thalach,
            exang,
            oldpeak,
            slope,
            ca,
            thal
        ]])

        prediction = model.predict(features)[0]

        probability = float(model.predict_proba(features)[0].max())

        if prediction == 1:

            result = "Heart Disease"

            st.error("⚠️ High Risk of Heart Disease")

        else:

            result = "No Heart Disease"

            st.success("✅ Low Risk")

        st.progress(probability)

        st.metric(
            "Confidence",
            f"{probability*100:.2f}%"
        )

        # Save prediction (4 arguments only)
        save_prediction(
            st.session_state.username,
            age,
            result,
            probability
        )

        # Generate PDF
        pdf = generate_report(
            st.session_state.username,
            age,
            result,
            probability
        )

        with open(pdf, "rb") as file:

            st.download_button(
                "📄 Download Report",
                file,
                file_name=pdf,
                mime="application/pdf"
            )

    st.markdown("</div>", unsafe_allow_html=True)