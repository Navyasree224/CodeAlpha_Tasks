import streamlit as st
import pandas as pd
from utils.database import get_history

def show_history_page():

    st.title("📜 Prediction History")

    history = get_history(st.session_state.username)

    if len(history) == 0:
        st.info("No prediction history found.")
        return

    df = pd.DataFrame(
        history,
        columns=[
            "Age",
            "Prediction",
            "Confidence",
            "Date"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )