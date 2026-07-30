import os
import streamlit as st


def create_sidebar():

    # -------------------------
    # Logo
    # -------------------------

    logo_path = "assets/logo.png"

    if os.path.exists(logo_path):

        st.sidebar.image(
            logo_path,
            use_container_width=True
        )

    # -------------------------
    # Title
    # -------------------------

    st.sidebar.title(
        "🚦 Smart Traffic Monitoring"
    )

    st.sidebar.caption(
        "AI Powered Traffic Analytics"
    )

    st.sidebar.divider()

    # -------------------------
    # Navigation
    # -------------------------

    st.sidebar.subheader("📌 Navigation")

    st.sidebar.markdown("""
- 📊 Dashboard
- 📈 Analytics
- 🚑 Emergency Status
- 📥 Reports
- 🗄 Database
""")

    st.sidebar.divider()

    # -------------------------
    # Features
    # -------------------------

    st.sidebar.subheader("⚙ Features")

    st.sidebar.markdown("""
✅ YOLO Vehicle Detection

✅ ByteTrack Object Tracking

✅ Vehicle Counting

✅ Entry / Exit Counter

✅ Speed Estimation

✅ Traffic Density Analysis

✅ AI Traffic Signal

✅ Emergency Priority

✅ SQLite Database

✅ CSV / Excel / PDF Reports
""")

    st.sidebar.divider()

    # -------------------------
    # Developer
    # -------------------------

    st.sidebar.success(
        """
**Developed By**

Sharif Ullah

BS Artificial Intelligence
"""
    )

    st.sidebar.caption(
        "Version 1.0"
    )