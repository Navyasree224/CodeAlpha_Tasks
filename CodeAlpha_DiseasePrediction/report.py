import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ======================================================
# Generate PDF Report
# ======================================================

def generate_report(username, age, result, probability):

    filename = f"{username}_Heart_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>Heart Disease Prediction Report</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Patient Name:</b> {username}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Age:</b> {age}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Prediction:</b> {result}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Confidence:</b> {probability*100:.2f}%",
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            "This report is generated using a Machine Learning model for educational purposes only.",
            styles["Italic"]
        )
    )

    doc.build(story)

    return filename


# ======================================================
# Reports Page
# ======================================================

def show_report_page():

    st.title("📄 PDF Reports")

    st.write("Generate and download your heart disease prediction report.")

    username = st.text_input("Patient Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=25
    )

    result = st.selectbox(
        "Prediction Result",
        [
            "No Heart Disease",
            "Heart Disease"
        ]
    )

    probability = st.slider(
        "Confidence",
        0.0,
        1.0,
        0.85
    )

    if st.button("Generate PDF"):

        pdf_file = generate_report(
            username,
            age,
            result,
            probability
        )

        st.success("✅ PDF Generated Successfully!")

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="⬇ Download Report",
                data=file,
                file_name=pdf_file,
                mime="application/pdf"
            )