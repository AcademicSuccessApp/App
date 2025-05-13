import streamlit as st
from models.user import Student, Teacher

def login_page():
    st.title("Academic Success Prediction System")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Student", "Teacher"])
        
        if st.form_submit_button("Login"):
            if role == "Student":
                user = Student(username, password)
            else:
                user = Teacher(username, password)
                
            if user.login():
                st.session_state.authenticated = True
                st.session_state.user_role = role.lower()
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials!") 