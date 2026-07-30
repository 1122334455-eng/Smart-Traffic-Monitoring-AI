import streamlit as st

from database.users import UserDatabase


def register():

    st.title("🚦 Smart Traffic Monitoring")

    st.subheader("📝 Create Admin Account")


    username = st.text_input(
        "Username"
    )


    password = st.text_input(
        "Password",
        type="password"
    )


    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )


    if st.button(
        "Create Account",
        use_container_width=True
    ):


        if username == "" or password == "":

            st.warning(
                "Please fill all fields"
            )


        elif password != confirm_password:

            st.error(
                "Passwords do not match"
            )


        else:

            db = UserDatabase()


            result = db.add_user(
                username,
                password
            )


            db.close()


            if result:

                st.success(
                    "Admin account created successfully"
                )

                st.info(
                    "Now login with your account"
                )

            else:

                st.error(
                    "Username already exists"
                )