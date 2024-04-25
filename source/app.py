import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('data/Connections.csv')

df["Connected On"] = pd.to_datetime(df["Connected On"])
df["Year"] = df["Connected On"].dt.year
df["Month"] = df["Connected On"].dt.month_name()
df["Day"] = df["Connected On"].dt.day_name()

# Basic data cleaning
df = df.drop(columns=['URL', 'Email Address'],inplace=False)
df = df.dropna()
st.dataframe(df)

# Number of connections made in each year
n_connections_per_year = df["Year"].value_counts().sort_index()

# Number of connections made monthly
n_connections_per_month = df["Month"].value_counts().sort_index()

# Number of connections made based on day of the week
n_connections_per_day = df["Day"].value_counts()

# Create a list of all months in chronological order
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_map = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
  }


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_of_week_map = {
  "Monday": 0,
  "Tuesday": 1,
  "Wednesday": 2,
  "Thursday": 3,
  "Friday": 4,
  "Saturday": 5,
  "Sunday": 6
}

# Title of the Streamlit App
st.title('LinkedIn Connection Insights')

# Connections per Company
connections_per_company = df['Company'].value_counts().head(20).sort_values(ascending=True)
fig1 = px.bar(connections_per_company, title="Top 10 Companies by Connections", orientation='h')
st.plotly_chart(fig1,use_container_width=True)

# Connections Over Time
# connections_over_time = df.groupby(df['Connected On'].dt.to_period("M")).size()
# fig2 = px.line(connections_over_time, title="Connections Over Time")
# st.plotly_chart(fig2)

# Display details about Position
positions_distribution = df['Position'].value_counts().head(10)
fig3 = px.pie(positions_distribution, names=positions_distribution.index, title="Top 10 Positions Held by Connections")
st.plotly_chart(fig3)
