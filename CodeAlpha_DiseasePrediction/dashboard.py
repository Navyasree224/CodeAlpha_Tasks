import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

def show_dashboard():

    st.title("📊 Heart Disease Analytics Dashboard")
    st.markdown("---")

    conn = sqlite3.connect("database/users.db")

    try:
        df = pd.read_sql_query("SELECT * FROM history", conn)
    except:
        st.error("History table not found.")
        conn.close()
        return

    conn.close()

    if df.empty:
        st.warning("No prediction history available.")
        return

    # ==========================
    # KPI CARDS
    # ==========================

    total = len(df)
    positive = len(df[df["prediction"] == "Heart Disease"])
    negative = total - positive
    avg_age = round(df["age"].mean(), 1)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("👥 Total Patients", total)

    with c2:
        st.metric("❤️ Positive Cases", positive)

    with c3:
        st.metric("💚 Healthy Cases", negative)

    with c4:
        st.metric("🎂 Average Age", avg_age)

    st.markdown("---")

    # ==========================
    # TABLE
    # ==========================

    st.subheader("📋 Prediction History")

    st.dataframe(
        df,
        use_container_width=True,
        height=350
    )

    st.markdown("---")

    # ==========================
    # PIE + SCATTER
    # ==========================

    left, right = st.columns(2)

    with left:

        fig1 = px.pie(
            df,
            names="prediction",
            hole=0.45,
            title="Prediction Distribution"
        )

        fig1.update_layout(
            height=500,
            legend_title="Prediction"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with right:

        fig2 = px.scatter(
            df,
            x="age",
            y="probability",
            color="prediction",
            size="probability",
            hover_data=["username"],
            title="Age vs Prediction Probability"
        )

        fig2.update_layout(
            height=500
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.markdown("---")

    # ==========================
    # BAR CHART
    # ==========================

    count_df = (
        df["prediction"]
        .value_counts()
        .reset_index()
    )

    count_df.columns = ["Prediction", "Count"]

    fig3 = px.bar(
        count_df,
        x="Prediction",
        y="Count",
        text="Count",
        title="Prediction Count"
    )

    fig3.update_layout(
        height=500
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================
    # AGE DISTRIBUTION
    # ==========================

    fig4 = px.histogram(
        df,
        x="age",
        nbins=10,
        title="Age Distribution"
    )

    fig4.update_layout(
        height=450
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )