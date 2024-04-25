import streamlit as st
import pandas as pd
import plotly.express as px

# Load your data here
def load_data():
    # Replace the file path with your LinkedIn CSV file path
    return pd.read_csv('data/Connections.csv')

df = load_data()

# Basic data cleaning
df['Connected On'] = pd.to_datetime(df['Connected On'])
df.dropna(subset=['Company', 'Position'], inplace=True)  # Remove rows where 'Company' or 'Position' is missing

# Title of the Streamlit App
st.title('LinkedIn Connection Insights')

# Connections per Company
connections_per_company = df['Company'].value_counts().head(20).sort_values(ascending=True)
fig1 = px.bar(connections_per_company, title="Top 10 Companies by Connections", orientation='h')
st.plotly_chart(fig1)

# Connections Over Time
# connections_over_time = df.groupby(df['Connected On'].dt.to_period("M")).size()
# fig2 = px.line(connections_over_time, title="Connections Over Time")
# st.plotly_chart(fig2)

# Display details about Position
positions_distribution = df['Position'].value_counts().head(10)
fig3 = px.pie(positions_distribution, names=positions_distribution.index, title="Top 10 Positions Held by Connections")
st.plotly_chart(fig3)
