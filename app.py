import streamlit as st
import pandas as pd
import plotly.express as px

# Load your data
xls = pd.ExcelFile('LCT.xlsx')
pangsa = pd.read_excel(xls, 'Pangsa Transaksi')
nasabah = pd.read_excel(xls, 'Total Pelaku Looker')
avgNasabah = pd.read_excel(xls, 'Rerata Nasabah LCT Bulanan')
transaksi = pd.read_excel(xls, 'Total Transaksi Looker')
avgTransaksi = pd.read_excel(xls, 'Rerata Transaksi LCT Bulanan')

# Function to create line graph
def visualize_line(data_sheet, xaxis, yaxis, title):
    data_sheet.columns = data_sheet.iloc[0].astype(str)
    data_sheet = data_sheet.iloc[1:]
    data_sheet = data_sheet.dropna(subset=['Negara'])

    tabel = pd.melt(data_sheet, id_vars=['Negara'], var_name='Year', value_name='Value')
    tabel.rename(columns={'Negara': 'Country'}, inplace=True)
    tabel = tabel[tabel['Year'] != 'Grand Total']
    tabel = tabel[tabel['Country'] != 'Grand Total']
    tabel['Year'] = tabel['Year'].astype(float).astype(int)  
    tabel['Year'] = pd.to_datetime(tabel['Year'], format='%Y')  

    fig = px.line(tabel, x='Year', y='Value', title=title, color='Country', width=1000, height=600, markers=True)
    fig.update_layout(title_x=0.5, xaxis_title=xaxis, yaxis_title=yaxis)

    return fig

# Function to create bar graph
def visualize_bar(data_sheet, xaxis, yaxis, title):
    data_sheet.columns = data_sheet.iloc[0].astype(str)
    data_sheet = data_sheet.iloc[1:]
    data_sheet = data_sheet.dropna(subset=['Negara'])

    tabel = pd.melt(data_sheet, id_vars=['Negara'], var_name='Year', value_name='Value')
    tabel.rename(columns={'Negara': 'Country'}, inplace=True)
    tabel = tabel[tabel['Year'] != 'Grand Total']
    tabel = tabel[tabel['Country'] != 'Grand Total']
    tabel['Year'] = tabel['Year'].astype(float).astype(int)  
    tabel['Year'] = pd.to_datetime(tabel['Year'], format='%Y')  

    fig = px.bar(tabel, x='Year', y='Value', title=title, color='Country', width=1000, height=600, barmode='group')
    fig.update_layout(title_x=0.5, xaxis_title=xaxis, yaxis_title=yaxis, legend=dict(
        title=None, orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5
    ))

    return fig

# Sidebar
st.sidebar.image('assets/BI_Logo.png', use_column_width=True)
st.sidebar.title('Sidebar')
selected_countries = st.sidebar.multiselect('Negara', ['Jepang', 'Malaysia', 'Thailand', 'Tiongkok'])
selected_years = st.sidebar.multiselect('Tahun', ['2018', '2019', '2020', '2021', '2022', '2023', '2024'])

# Main Content
st.title('LCT Overview')

# Display the graphs
st.plotly_chart(visualize_bar(transaksi, 'Year', 'Total Transaksi', 'Total Transaksi'))
st.plotly_chart(visualize_bar(nasabah, 'Year', 'Total Nasabah', 'Total Nasabah'))
st.plotly_chart(visualize_bar(avgNasabah, 'Year', 'Average Nasabah', 'Average Nasabah'))
st.plotly_chart(visualize_bar(avgTransaksi, 'Year', 'Average Transaksi', 'Average Transaksi'))
