import streamlit as st
import psycopg2

st.set_page_config(page_title="Add Student", page_icon="👤")

def get_connection():
    return psycopg2.connect(st.secrets["SLDB_URL"])

st.title("👤 Add a New Student")

with st.form("add_student_form"):
    name = st.text_input("Student Name")
    email = st.text_input("Student Email")
    submitted = st.form_submit_button("Add Student")

    if submitted:
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid_email = re.match(email_pattern, email)

        if not name or not email:
            st.warning("Please fill in both fields.")
        elif not is_valid_email:
            st.warning("⚠️ Please enter a valid email address (e.g., student@example.com).")
        else:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO students10 (name, email) VALUES (%s, %s);",
                    (name, email)
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success(f"✅ Student '{name}' added successfully!")
            except psycopg2.errors.UniqueViolation:
                st.error("⚠️ A student with that email already exists.")
            except Exception as e:
                st.error(f"Error: {e}")
