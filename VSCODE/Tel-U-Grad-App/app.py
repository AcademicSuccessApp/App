import streamlit as st
import pandas as pd
import plotly.express as px
from models.prediction import PredictionModel

def main():
    st.set_page_config(
        page_title="Academic Success Prediction",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("Academic Success Prediction System")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Input Data", "Prediction Results", "Data Visualization"])
    
    with tab1:
        show_data_input()
    
    with tab2:
        show_prediction_results()
    
    with tab3:
        show_visualizations()

def show_data_input():
    st.header("Student Academic Data")
    
    with st.form("academic_data"):
        col1, col2 = st.columns(2)
        
        with col1:
            gpa = st.number_input("GPA", 0.0, 4.0, 3.0, help="Current Grade Point Average")
            attendance = st.number_input("Attendance (%)", 0, 100, 80, help="Class attendance percentage")
            credits = st.number_input("Total Credits", 0, 160, 100, help="Number of credits completed")
        
        with col2:
            study_hours = st.number_input("Study Hours/Week", 0, 100, 20, help="Average study hours per week")
            extracurricular = st.selectbox(
                "Extracurricular Activities",
                ["None", "Low", "Medium", "High"],
                help="Level of involvement in extracurricular activities"
            )
            internship = st.checkbox("Completed Internship", help="Whether student has completed an internship")
        
        if st.form_submit_button("Predict Success"):
            # Store the input data in session state
            st.session_state.input_data = {
                "gpa": gpa,
                "attendance": attendance,
                "credits": credits,
                "study_hours": study_hours,
                "extracurricular": extracurricular,
                "internship": internship
            }
            st.success("Data submitted for prediction!")

def show_prediction_results():
    st.header("Prediction Results")
    
    if 'input_data' in st.session_state:
        # Create prediction model instance
        model = PredictionModel()
        prediction = model.predict(st.session_state.input_data)
        
        # Display prediction results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Graduation Probability", f"{prediction:.1%}")
        
        with col2:
            status = "Likely to Graduate" if prediction > 0.7 else "At Risk"
            st.metric("Status", status)
        
        with col3:
            recommendation = get_recommendations(st.session_state.input_data)
            st.info(f"Recommendation: {recommendation}")

def show_visualizations():
    st.header("Performance Analytics")
    
    if 'input_data' in st.session_state:
        # Create sample historical data for visualization
        data = {
            'Metric': ['GPA', 'Attendance', 'Credits', 'Study Hours'],
            'Value': [
                st.session_state.input_data['gpa'],
                st.session_state.input_data['attendance'],
                st.session_state.input_data['credits'],
                st.session_state.input_data['study_hours']
            ],
            'Target': [3.5, 85, 120, 25]  # Example target values
        }
        
        df = pd.DataFrame(data)
        
        # Create bar chart comparing current values vs targets
        fig = px.bar(
            df,
            x='Metric',
            y=['Value', 'Target'],
            barmode='group',
            title='Current Performance vs Targets',
            labels={'value': 'Score', 'variable': 'Type'}
        )
        
        st.plotly_chart(fig)

def get_recommendations(data):
    """Generate recommendations based on input data"""
    recommendations = []
    
    if data['gpa'] < 3.0:
        recommendations.append("Focus on improving GPA")
    if data['attendance'] < 80:
        recommendations.append("Increase class attendance")
    if data['study_hours'] < 20:
        recommendations.append("Increase study hours")
    
    return " | ".join(recommendations) if recommendations else "Keep up the good work!"

if __name__ == "__main__":
    main() 