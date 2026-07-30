"""
=========================================
Emergency Status Card
Smart Traffic Monitoring Dashboard
=========================================
"""

import streamlit as st


def show_emergency_card(status=False, vehicle="None"):


    st.subheader("🚑 Emergency Vehicle Status")


    if status:

        st.success("🟢 PRIORITY MODE ACTIVE")


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Status",
                "DETECTED"
            )


        with col2:

            st.metric(
                "Vehicle",
                vehicle.upper()
            )


        st.info(
            "🚦 Signal Override: GREEN"
        )


    else:

        st.warning(
            "⚪ No Emergency Vehicle"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Status",
                "CLEAR"
            )


        with col2:

            st.metric(
                "Priority",
                "NORMAL"
            )