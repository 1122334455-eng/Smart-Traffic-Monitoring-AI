import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


import streamlit as st
import pandas as pd

from streamlit_autorefresh import st_autorefresh

from database.database import TrafficDatabase


from sidebar import create_sidebar
from emergency_card import show_emergency_card
from login import login
from register import register
from admin_panel import admin_panel


from charts import (
    vehicle_chart,
    density_chart,
    speed_chart
)

from heatmap import vehicle_heatmap



st.set_page_config(
    page_title="Smart Traffic Monitoring",
    page_icon="🚦",
    layout="wide"
)



# ==============================
# Load Database Data
# ==============================

def load_data():

    db = TrafficDatabase()

    data = db.fetch_all()

    db.close()

    return data




def read_file(path):

    with open(path,"rb") as file:
        return file.read()




# ==============================
# Main Dashboard
# ==============================

def main():


    if "logged_in" not in st.session_state:

        st.session_state["logged_in"] = False



    if not st.session_state["logged_in"]:


        option = st.sidebar.radio(
            "Select Option",
            [
                "Login",
                "Create Admin"
            ]
        )


        if option == "Create Admin":

            register()

        else:

            login()


        return



    # Auto Refresh

    st_autorefresh(
        interval=2000,
        key="traffic_dashboard"
    )
    st.write(
        "Last Refresh:",
        pd.Timestamp.now()
    )



    create_sidebar()



    if st.sidebar.button("🚪 Logout"):

        st.session_state["logged_in"] = False

        st.rerun()



    # ==============================
    # Header
    # ==============================


    st.title(
        "🚦 Smart Traffic Monitoring Dashboard"
    )


    st.markdown(
    """
    ### AI Powered Real-Time Vehicle Analytics

    YOLO Object Detection |
    ByteTrack Tracking |
    Vehicle Counting |
    Speed Estimation |
    Traffic Density |
    Violation Detection |
    SQLite Database

    ---
    """
    )



    # ==============================
    # Database Load
    # ==============================


    data = load_data()



    if len(data) == 0:

        st.warning(
            "No traffic data available"
        )

        return




    # ==============================
    # DataFrame
    # ==============================


    df = pd.DataFrame(

        data,

        columns=[

            "ID",

            "Session",

            "Vehicle_ID",

            "Vehicle",

            "Speed",

            "Violation",

            "Density",

            "Entry",

            "Exit",

            "Timestamp"

        ]

    )




    # ==============================
    # Session Filter
    # ==============================


    st.subheader(
        "🎯 Session Analytics"
    )


    sessions = sorted(
        df["Session"].unique(),
        reverse=True
    )


    selected_session = st.selectbox(

        "Select Session",

        sessions,

        index=0,

        key=f"session_{sessions[0]}"

    )



    df = df[
        df["Session"] == selected_session
    ]



    st.success(
        f"Showing Session #{selected_session}"
    )



    st.divider()



    # ==============================
    # Metrics
    # ==============================


    st.subheader(
        "📊 Live Statistics"
    )


    col1,col2,col3,col4 = st.columns(4)



    with col1:

        st.metric(

            "🚗 Total Vehicles",

            len(df)

        )



    with col2:

        st.metric(

            "🚨 Violations",

            len(
                df[
                    df["Violation"]=="YES"
                ]
            )

        )



    with col3:

        st.metric(

            "➡ Entry",

            int(df["Entry"].sum())

        )



    with col4:

        st.metric(

            "⬅ Exit",

            int(df["Exit"].sum())

        )




    col5,col6,col7,col8 = st.columns(4)



    with col5:

        st.metric(
            "🚙 Cars",
            len(
                df[
                df["Vehicle"]=="car"
                ]
            )
        )



    with col6:

        st.metric(
            "🚚 Trucks",
            len(
                df[
                df["Vehicle"]=="truck"
                ]
            )
        )



    with col7:

        st.metric(
            "🚌 Bus",
            len(
                df[
                df["Vehicle"]=="bus"
                ]
            )
        )



    with col8:

        st.metric(
            "🏍 Motorcycle",
            len(
                df[
                df["Vehicle"]=="motorcycle"
                ]
            )
        )



    st.divider()



    # ==============================
    # Emergency
    # ==============================


    show_emergency_card(

        status=True,

        vehicle="AMBULANCE"

    )


    st.divider()



    admin_panel()



    st.divider()



    # ==============================
    # Charts
    # ==============================


    st.subheader(
        "📈 Traffic Analytics"
    )


    c1,c2 = st.columns(2)



    with c1:


        st.plotly_chart(

            vehicle_chart(df),

            use_container_width=True

        )



    with c2:


        st.plotly_chart(

            density_chart(df),

            use_container_width=True

        )



    st.plotly_chart(

        speed_chart(df),

        use_container_width=True

    )



    st.divider()



    st.subheader(
        "🗺 Vehicle Heatmap"
    )



    st.plotly_chart(

        vehicle_heatmap(df),

        use_container_width=True

    )



    st.divider()



    # ==============================
    # Records
    # ==============================


    st.subheader(
        "📋 Traffic Records"
    )


    search = st.text_input(
        "🔍 Search Vehicle"
    )



    if search:


        filtered_df = df[
            df["Vehicle"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    else:

        filtered_df = df




    st.dataframe(

        filtered_df,

        use_container_width=True

    )




    # ==============================
    # Reports
    # ==============================


    st.divider()


    st.subheader(
        "📥 Download Reports"
    )



    col1,col2,col3 = st.columns(3)



    with col1:

        if os.path.exists(
            "output/traffic_report.csv"
        ):

            st.download_button(

                "⬇ CSV",

                read_file(
                    "output/traffic_report.csv"
                ),

                "traffic_report.csv"

            )



    with col2:

        if os.path.exists(
            "output/traffic_report.xlsx"
        ):

            st.download_button(

                "⬇ Excel",

                read_file(
                    "output/traffic_report.xlsx"
                ),

                "traffic_report.xlsx"

            )



    with col3:

        if os.path.exists(
            "output/traffic_report.pdf"
        ):

            st.download_button(

                "⬇ PDF",

                read_file(
                    "output/traffic_report.pdf"
                ),

                "traffic_report.pdf"

            )





if __name__=="__main__":

    main()