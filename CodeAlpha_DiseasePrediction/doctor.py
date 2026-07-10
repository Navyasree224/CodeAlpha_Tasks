import streamlit as st


def show_doctor_page():

    st.title("🩺 Doctor Recommendation")

    st.subheader("🏥 Recommended Hospitals")

    hospitals = [
        {
            "name": "Apollo Hospitals",
            "city": "Hyderabad",
            "speciality": "Cardiology",
            "phone": "+91-40-23607777"
        },
        {
            "name": "Yashoda Hospitals",
            "city": "Hyderabad",
            "speciality": "Heart Institute",
            "phone": "+91-40-45674567"
        },
        {
            "name": "CARE Hospitals",
            "city": "Hyderabad",
            "speciality": "Cardiac Sciences",
            "phone": "+91-40-68106588"
        },
        {
            "name": "KIMS Hospitals",
            "city": "Hyderabad",
            "speciality": "Cardiology",
            "phone": "+91-40-44885000"
        }
    ]

    for hospital in hospitals:

        st.markdown("---")

        st.markdown(f"### 🏥 {hospital['name']}")

        st.write(f"📍 City : {hospital['city']}")
        st.write(f"❤️ Speciality : {hospital['speciality']}")
        st.write(f"📞 Contact : {hospital['phone']}")

    st.subheader("👨‍⚕️ Recommended Cardiologists")

    doctors = [
        "Dr. A. Kumar",
        "Dr. Priya Reddy",
        "Dr. Rajesh Sharma",
        "Dr. Srinivas Rao"
    ]

    for doctor in doctors:
        st.write(f"✅ {doctor}")