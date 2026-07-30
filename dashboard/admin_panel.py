import streamlit as st
import sqlite3


DATABASE_PATH = "database/traffic.db"


def admin_panel():

    st.subheader("👥 Admin Management")

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT id, username, created_at
        FROM users
        ORDER BY id
        """
    )

    admins = cursor.fetchall()


    if len(admins) == 0:

        st.warning("No Admin Found")

    else:

        st.success(
            f"Total Admins : {len(admins)}"
        )

        st.divider()


        for admin in admins:

            admin_id = admin[0]
            username = admin[1]
            created = admin[2]

            col1, col2 = st.columns([4,1])

            with col1:

                st.write(
                    f"👤 {username}"
                )

                st.caption(
                    f"Created : {created}"
                )

            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{admin_id}"
                ):

                    cursor.execute(
                        """
                        DELETE FROM users
                        WHERE id=?
                        """,
                        (admin_id,)
                    )

                    conn.commit()

                    st.success(
                        "Admin Deleted"
                    )

                    st.rerun()

            st.divider()


    conn.close()