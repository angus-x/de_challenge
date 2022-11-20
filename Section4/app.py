import json
import requests
import pandas as pd
import streamlit as st
import plotly.express as px


url = 'https://api.covid19api.com/country/singapore'


def extract_data(url):
    r = requests.get(url)
    data = json.loads(r.content)
    df = pd.DataFrame(data)
    return df


data = extract_data(url)
data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
values = data[['Confirmed', 'Deaths']]

# set up the chart
st.header("COVID-19 in Singapore - cumulative case counts and deaths")

with st.container():
    fig1 = px.line(data, x='Date', y=['Confirmed'])
    st.plotly_chart(fig1, use_container_width=True)
    fig2 = px.bar(data, x='Date', y=['Deaths'])
    st.plotly_chart(fig2, use_container_width=True)
