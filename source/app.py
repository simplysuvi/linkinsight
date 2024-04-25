import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
fig1 = px.bar(connections_per_company, title="Top 20 Companies by Connections", orientation='h')
st.plotly_chart(fig1,use_container_width=True)

# Calculate average connections per day per year
avg_connections_per_day_per_year = n_connections_per_year.divide(365)
fig = px.line(
    avg_connections_per_day_per_year,
    labels={'index': 'Year', 'value': 'Average Connections per Day'},
    title='Average LinkedIn Connections Daily Trend',
    markers=True
)
fig.update_traces(mode='lines+markers+text', textposition='top center')
st.plotly_chart(fig, use_container_width=True)


# Calculate the number of connections made each day in each year
n_connections_per_day_per_year = df.groupby(["Year", "Day"]).size()
data = []
for year in range(2016, 2025):
    for day in days:
        data.append({
            'Year': year,
            'Day of Week': day,
            'Connections': n_connections_per_day_per_year.get((year, day), 0)
        })

df1 = pd.DataFrame(data)
fig = px.line(
    df1, 
    x="Day of Week", 
    y="Connections", 
    color="Year",
    title="Number of LinkedIn Connections Made Each Day of the Week (2016-2024)",
    markers=True
)
fig.update_layout(
    xaxis_title="Day of Week",
    yaxis_title="Number of Connections",
    width=1200,
    height=700
)

st.plotly_chart(fig, use_container_width=True)



# Calculate the cumulative sum of the number of connections made in each year
total_connections_per_year = n_connections_per_year.cumsum()
fig = go.Figure()
fig.add_trace(go.Bar(
    x=total_connections_per_year.index,
    y=total_connections_per_year.values,
    name='Cumulative Connections',
    marker_color='lightgreen'
))
fig.add_trace(go.Scatter(
    x=total_connections_per_year.index,
    y=total_connections_per_year.values,
    mode='lines+markers',
    name='Total Connections',
    line_color='green'
))
fig.update_layout(
    title="Total LinkedIn Connections in Each Year",
    xaxis_title="Year",
    yaxis_title="Total Number of Connections",
    width=1400,
    height=800
)
st.plotly_chart(fig, use_container_width=True)



# Displaying Top 20 Positions
top_positions = df['Position'].value_counts().head(20).sort_values()
fig1 = px.bar(top_positions, orientation='h',
              labels={'value': 'Number of Connections in that Position', 'index': 'Position'},
              title="Top 20 Positions within the Connections",
              color_discrete_sequence=px.colors.sequential.Flake)
fig1.update_layout(xaxis_title="Number of Connections in that Position",
                   yaxis_title="Position",
                   height=700)

# Displaying Top 20 Companies
top_companies = df['Company'].value_counts().head(20).sort_values()
fig2 = px.bar(top_companies, orientation='h',
              labels={'value': 'Number of Connections in Company', 'index': 'Company'},
              title="Top 20 Companies Connections Work at",
              color_discrete_sequence=px.colors.sequential.Flake)
fig2.update_layout(xaxis_title="Number of Connections in Company",
                   yaxis_title="Company",
                   height=700)

st.plotly_chart(fig1)
st.plotly_chart(fig2)