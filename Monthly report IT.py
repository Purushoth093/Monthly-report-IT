import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Function to generate the report
def generate_monthly_report(performance_data, incident_data):
    # Ensure the date columns are in datetime format
    performance_data['Date'] = pd.to_datetime(performance_data['Date'])
    incident_data['Date'] = pd.to_datetime(incident_data['Date'])
    
    # Get the current month and year
    today = datetime.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    
    # Filter data for the current month
    monthly_performance = performance_data[(performance_data['Date'] >= first_day_of_month) & (performance_data['Date'] <= last_day_of_month)]
    monthly_incidents = incident_data[(incident_data['Date'] >= first_day_of_month) & (incident_data['Date'] <= last_day_of_month)]

    # Summarize system performance data
    performance_summary = monthly_performance.groupby('System').agg(
        Avg_CPU_Usage=('CPU_Usage', 'mean'),
        Max_Memory_Usage=('Memory_Usage', 'max')
    ).reset_index()

    # Summarize incident data
    incident_summary = monthly_incidents.groupby('Category').agg(
        Total_Incidents=('Incident_ID', 'count'),
        Avg_Response_Time=('Response_Time', 'mean')
    ).reset_index()

    return performance_summary, incident_summary

# Streamlit app
st.title('IT Monthly Report Generator')

# Upload CSV files
performance_file = st.file_uploader("Upload System Performance Data (CSV)", type="csv")
incident_file = st.file_uploader("Upload Incident Log Data (CSV)", type="csv")

if performance_file and incident_file:
    # Load data
    performance_data = pd.read_csv(performance_file)
    incident_data = pd.read_csv(incident_file)
    
    # Generate report
    performance_summary, incident_summary = generate_monthly_report(performance_data, incident_data)
    
    # Display the results
    st.subheader('System Performance Summary')
    st.write(performance_summary)
    
    st.subheader('Incident Summary')
    st.write(incident_summary)
else:
    st.info('Please upload both CSV files to generate the report.')
