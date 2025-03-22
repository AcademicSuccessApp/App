import streamlit as st
import pandas as pd
import plotly.express as px
from models.prediction import PredictionModel

def student_dashboard():
    st.title(f"Welcome, {st.session_state.username}!")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Profile", "Academic Data", "Prediction", "Visualizations"]
    )
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.username = None
        st.rerun()
    
    if page == "Academic Data":
        show_academic_data_input()
    elif page == "Prediction":
        show_prediction_page()
    elif page == "Visualizations":
        show_visualizations()
    else:
        show_profile()

def show_academic_data_input():
    st.header("Academic Data Input")
    
    with st.form("academic_data"):
        gpa = st.number_input("GPA", 0.0, 4.0, 3.0)
        attendance = st.number_input("Attendance (%)", 0, 100, 80)
        credits = st.number_input("Total Credits", 0, 160, 100)
        
        if st.form_submit_button("Save Data"):
            # Save data logic here
            st.success("Data saved successfully!")

def show_prediction_page():
    st.header("Graduation Prediction")
    
    # Add prediction logic here
    model = PredictionModel()
    prediction = model.predict({"gpa": 3.5, "attendance": 85, "credits": 120})
    
    st.metric("Graduation Probability", f"{prediction:.2%}") 