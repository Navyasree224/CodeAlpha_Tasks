import streamlit as st
import numpy as np
import pandas as pd
import cv2
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from predict import predict_digit

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Handwritten Digit Recognition",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#E8F4FF,#CDE7FF,#A8D4FF);
}

section[data-testid="stSidebar"]{
background:#0F172A;
}

section[data-testid="stSidebar"] *{
color:white;
}

.title{
text-align:center;
font-size:46px;
font-weight:bold;
color:#0A3D91;
}

.subtitle{
text-align:center;
font-size:20px;
color:#455A64;
margin-bottom:20px;
}

.card{
background:white;
padding:25px;
border-radius:18px;
box-shadow:0px 8px 20px rgba(0,0,0,0.15);
}

.result-card{
background:#E8FFF1;
padding:20px;
border-radius:15px;
font-size:28px;
font-weight:bold;
text-align:center;
color:#0D652D;
}

.footer{
text-align:center;
font-size:16px;
color:#555;
padding-top:30px;
}

.metric-box{
background:white;
padding:15px;
border-radius:15px;
box-shadow:0px 4px 12px rgba(0,0,0,.1);
text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🤖 AI Dashboard")

st.sidebar.success("✅ CNN Model Loaded")

st.sidebar.markdown("---")

st.sidebar.subheader("📌 Project Information")

st.sidebar.write("**Model :** CNN")

st.sidebar.write("**Dataset :** MNIST")

st.sidebar.write("**Framework :** TensorFlow")

st.sidebar.write("**Frontend :** Streamlit")

st.sidebar.write("**Accuracy :** 99.2%")

st.sidebar.markdown("---")

st.sidebar.info(
"""
✍ Draw any digit from **0–9**

OR

📤 Upload a handwritten digit image

Then click **Predict**
"""
)

st.sidebar.markdown("---")

st.sidebar.subheader("📜 Prediction History")

if len(st.session_state.history)==0:
    st.sidebar.write("No predictions yet.")
else:
    for item in st.session_state.history[::-1]:
        st.sidebar.write(item)

# =====================================================
# PREMIUM HEADER
# =====================================================

st.markdown("""
<div style="
padding:35px;
border-radius:25px;
background:linear-gradient(135deg,#2563EB,#3B82F6,#60A5FA);
color:white;
text-align:center;
box-shadow:0 15px 35px rgba(0,0,0,.25);
">

<h1 style="font-size:52px;">
🤖 AI Handwritten Digit Recognition
</h1>

<h4>
Deep Learning using CNN • TensorFlow • MNIST Dataset
</h4>

<p style="font-size:18px;">
Draw any handwritten digit or upload an image to let the AI recognize it instantly.
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================================
# AI DASHBOARD CARDS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("""
### 🎯 Accuracy

**99.2%**
""")

with c2:
    st.success("""
### 🧠 Model

**CNN**
""")

with c3:
    st.warning("""
### 📚 Dataset

**MNIST**
""")

with c4:
    st.error("""
### 🔢 Classes

**10 Digits**
""")

st.write("")
# ---------------------------------------------------
# TOP METRICS
# ---------------------------------------------------

m1,m2,m3 = st.columns(3)

with m1:
    st.metric("Model Accuracy","99.2%")

with m2:
    st.metric("Dataset","MNIST")

with m3:
    st.metric("Classes","10 Digits")

st.write("")


# ---------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------

left_col, right_col = st.columns([1.25, 1])

# ==========================
# LEFT PANEL
# ==========================

with left_col:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("✍ Draw a Digit")

    canvas_result = st_canvas(
        fill_color="black",
        stroke_width=18,
        stroke_color="white",
        background_color="black",
        width=350,
        height=350,
        drawing_mode="freedraw",
        key="canvas",
    )

    st.write("")

    uploaded_file = st.file_uploader(
        "📤 Or Upload an Image",
        type=["png", "jpg", "jpeg"]
    )

    st.write("")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        predict_btn = st.button(
            "🚀 Predict",
            use_container_width=True,
            type="primary"
        )

    with col_btn2:
        clear_btn = st.button(
            "🧹 Clear Canvas",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# RIGHT PANEL
# ==========================

with right_col:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("🤖 AI Prediction")

    result_box = st.empty()

    confidence_box = st.empty()

    st.write("")

    progress_bar = st.empty()

    st.write("")

    st.subheader("📊 Probability Chart")

    chart_area = st.empty()

    st.write("")

    table_area = st.empty()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# CLEAR BUTTON
# ---------------------------------------------------

if clear_btn:

    st.session_state.history = []

    st.rerun()

    # ---------------------------------------------------
# PREDICTION
# ---------------------------------------------------

if predict_btn:

    img = None

    # ===== Canvas Image =====
    if canvas_result.image_data is not None:

        img = canvas_result.image_data[:, :, 0]

        img = cv2.resize(img.astype("uint8"), (28, 28))

        img = 255 - img

    # ===== Uploaded Image =====
    elif uploaded_file is not None:

        image = Image.open(uploaded_file).convert("L")

        image = image.resize((28, 28))

        img = np.array(image)

        img = 255 - img

    # ===== Predict =====
    if img is not None:

        digit, confidence, probabilities = predict_digit(img)

        st.session_state.history.append(
            f"Digit {digit} ({confidence*100:.2f}%)"
        )

        result_box.markdown(f"""
        <div class="result-card">
        🎯 Prediction : {digit}
        </div>
        """, unsafe_allow_html=True)

        confidence_box.write(
            f"### Confidence : {confidence*100:.2f}%"
        )

        progress_bar.progress(float(confidence))

        chart_df = pd.DataFrame({
            "Digit": list(range(10)),
            "Probability": probabilities
        })

        chart_area.bar_chart(
            chart_df.set_index("Digit")
        )

        table_area.dataframe(
            chart_df,
            use_container_width=True
        )

    else:

        st.warning(
            "Please draw a digit or upload an image."
        )

# ---------------------------------------------------
# DOWNLOAD HISTORY
# ---------------------------------------------------

if len(st.session_state.history) > 0:

    st.write("")

    st.subheader("📥 Download Prediction History")

    history_df = pd.DataFrame({
        "Prediction History":
        st.session_state.history
    })

    st.download_button(
        label="⬇ Download CSV",
        data=history_df.to_csv(index=False),
        file_name="prediction_history.csv",
        mime="text/csv",
        use_container_width=True
    )

# ---------------------------------------------------
# PROJECT INFORMATION
# ---------------------------------------------------

st.write("")
st.markdown("---")

st.subheader("📚 About This Project")

colA, colB = st.columns(2)

with colA:

    st.info("""
### 🤖 CNN Model

This application uses a Convolutional Neural Network (CNN)
trained on the MNIST handwritten digit dataset.

The model predicts digits from **0–9** with
approximately **99% accuracy**.
""")

with colB:

    st.success("""
### 🛠 Technologies Used

- Python
- TensorFlow
- Keras
- Streamlit
- OpenCV
- NumPy
- Pandas
""")

st.markdown("---")

st.markdown("""
<div class='footer'>

<h2>🤖 AI Handwritten Digit Recognition</h2>

<p>
Deep Learning • CNN • TensorFlow • Streamlit
</p>

<p>
Developed by <b>P. Navya Sree</b> ❤️
</p>

</div>
""", unsafe_allow_html=True)