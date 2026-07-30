import streamlit as st

from database.users import UserDatabase


def login():

    st.title("🚦 Smart Traffic Monitoring")

    st.subheader("🔐 Admin Login")


    username = st.text_input(
        "Username"
    )


    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button(
        "Login",
        use_container_width=True
    ):

        db = UserDatabase()


        result = db.verify_user(
            username,
            password
        )


        db.close()


        if result:

            st.session_state["logged_in"] = True

            st.success(
                "Login Successful"
            )

            st.rerun()


        else:

            st.error(
                "Invalid Username or Password"
            )


    st.divider()


    st.info(
        "New Admin? Create your account from Register page."
    )