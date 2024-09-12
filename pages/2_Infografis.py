import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page layout to wide
st.set_page_config(layout="wide")



def add_logo():
    # Function to add a logo in the sidebar
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://upload.wikimedia.org/wikipedia/commons/3/39/BI_Logo.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
                background-size: 200px 60px; 
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()

# Utility function to check and handle the uploaded file
def check_and_upload_file():
    # Initialize session state for the uploaded file if not already set
    if 'uploaded_file' not in st.session_state:
        st.session_state['uploaded_file'] = None

    # File uploader
    uploaded_file = st.file_uploader('Upload file:', type=['xlsx'])

    # Store the uploaded file in session state
    if uploaded_file is not None:
        st.session_state['uploaded_file'] = uploaded_file
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    # Provide access to the file on each page
    if st.session_state['uploaded_file']:
        st.write(f"Using the file: {st.session_state['uploaded_file'].name}")
    else:
        st.write("No file uploaded.")

    # Optional: Button to clear the uploaded file from session state
    if st.button('Clear File'):
        del st.session_state['uploaded_file']
        st.success("File cleared.")

# Call the function to handle file upload at the beginning
check_and_upload_file()

# Proceed only if a file has been uploaded
if st.session_state['uploaded_file']:
    # Load data into session state
    xls = pd.ExcelFile(st.session_state['uploaded_file'])
    st.session_state['pangsa'] = pd.read_excel(xls, 'Pangsa Transaksi')
    st.session_state['nasabah'] = pd.read_excel(xls, 'Total Pelaku Looker')
    st.session_state['avgNasabah'] = pd.read_excel(xls, 'Rerata Nasabah LCT Bulanan')
    st.session_state['transaksi'] = pd.read_excel(xls, 'Total Transaksi Looker')
    st.session_state['avgTransaksi'] = pd.read_excel(xls, 'Rerata Transaksi LCT Bulanan')

    pangsa = st.session_state['pangsa']
    nasabah = st.session_state['nasabah']
    avgNasabah = st.session_state['avgNasabah']
    transaksi = st.session_state['transaksi']
    avgTransaksi = st.session_state['avgTransaksi']

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

        custom_colors = ['#ECE9DA', '#FFC20E', '#2F7DC1', '#F05559', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

        fig = px.line(tabel, x='Year', y='Value', title=title, color='Country', markers=True, color_discrete_sequence=custom_colors)
        fig.update_layout(title_x=0.5, xaxis_title=None, yaxis_title=yaxis)
        fig.update_yaxes(title=None)
        fig.update_layout(title={'x': 0.5}, xaxis_title=None, yaxis_title=yaxis, legend=dict(
            title=None, orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5
        ))
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,  # Centering the title
                'xanchor': 'center'
            }
        )

        fig.update_layout(xaxis=dict(tickvals=tabel['Year'].unique(), tickformat="%Y"))

        return fig

    # Function to create bar graph
    def visualize_bar(data_sheet, xaxis, yaxis, title):
        # Prepare the data
        data_sheet.columns = data_sheet.iloc[0].astype(str)
        data_sheet = data_sheet.iloc[1:].dropna(subset=['Negara'])
        tabel = pd.melt(data_sheet, id_vars=['Negara'], var_name='Year', value_name='Value')
        tabel.rename(columns={'Negara': 'Country'}, inplace=True)
        tabel = tabel[(tabel['Year'] != 'Grand Total') & (tabel['Country'] != 'Grand Total')]
        tabel['Year'] = pd.to_datetime(tabel['Year'].astype(float).astype(int), format='%Y')

        # Define custom colors
        custom_colors = ['#ECE9DA', '#FFC20E', '#2F7DC1', '#F05559', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

        # Create the Plotly bar chart
        fig = px.bar(tabel, x='Year', y='Value', title=title, color='Country', barmode='group', color_discrete_sequence=custom_colors)

        # Update the layout and formatting
        fig.update_layout(
            title={'text': title, 'x': 0.5, 'xanchor': 'center'},
            xaxis_title=None, yaxis_title=yaxis,
            legend=dict(title=None, orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            xaxis=dict(tickvals=tabel['Year'].unique(), tickformat="%Y"),
            plot_bgcolor='rgba(0, 0, 0, 0)',   # Set background to transparent if needed
            paper_bgcolor='rgba(0, 0, 0, 0)'   # Set background to transparent if needed
        )

        return fig

    # Main Content
    st.title('LCT Overview')

    # Create two columns for the first row of graphs
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(visualize_bar(transaksi, 'Year', 'Total Transaksi LCT ($USD Juta)', 'Total Transaksi'), use_container_width=True)
    with col2:
        st.plotly_chart(visualize_bar(nasabah, 'Year', 'Total Nasabah', 'Total Nasabah LCT (Pelaku Usaha)'), use_container_width=True)

    # Create two columns for the second row of graphs
    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(visualize_bar(avgNasabah, 'Year', 'Average Nasabah', 'Rerata Nasabah LCT (Pelaku Usaha)'), use_container_width=True)
    with col4:
        st.plotly_chart(visualize_bar(avgTransaksi, 'Year', 'Average Transaksi', 'Rerata Transaksi LCT ($USD Juta)'), use_container_width=True)

    # Additional graphs for Pangsa Transaksi
    st.plotly_chart(visualize_line(pangsa, 'Year', 'Pangsa Transaksi', 'Pangsa Transaksi'), use_container_width=True)
else:
    st.warning("Please upload an Excel file to proceed.")
