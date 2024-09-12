import streamlit as st
import pandas as pd
import plotly.express as px


# Set the page layout to wide
st.set_page_config(layout="wide")


with open("assets/style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

def add_logo():
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
    # Load your data
    xls = pd.ExcelFile(st.session_state['uploaded_file'])
    pangsa = pd.read_excel(xls, 'Pangsa Transaksi')
    nasabah = pd.read_excel(xls, 'Total Pelaku Looker')
    avgNasabah = pd.read_excel(xls, 'Rerata Nasabah LCT Bulanan')
    transaksi = pd.read_excel(xls, 'Total Transaksi Looker')
    avgTransaksi = pd.read_excel(xls, 'Rerata Transaksi LCT Bulanan')
    growthYOY = pd.read_excel(xls, 'Growth YoY')

    def total_latest_year(data_sheet):
        data_sheet.columns = data_sheet.iloc[0].astype(str)
        data_sheet = data_sheet.iloc[1:]
        data_sheet = data_sheet.dropna(subset=['Negara'])

        tabel = pd.melt(data_sheet, id_vars=['Negara'], var_name='Year', value_name='Value')
        tabel.rename(columns={'Negara': 'Country'}, inplace=True)
        tabel = tabel[tabel['Year'] != 'Grand Total']
        tabel = tabel[tabel['Country'] != 'Grand Total']
        tabel['Year'] = tabel['Year'].astype(float).astype(int)
        tabel['Year'] = pd.to_datetime(tabel['Year'], format='%Y')
        tabel['Year'] = tabel['Year'].dt.year

        # Get the latest year
        latest_year = tabel['Year'].max()
        return tabel[tabel['Year'] == latest_year].sum()['Value']

    def total_previous_year(data_sheet):
        data_sheet.columns = data_sheet.iloc[0].astype(str)
        data_sheet = data_sheet.iloc[1:]
        data_sheet = data_sheet.dropna(subset=['Negara'])

        tabel = pd.melt(data_sheet, id_vars=['Negara'], var_name='Year', value_name='Value')
        tabel.rename(columns={'Negara': 'Country'}, inplace=True)
        tabel = tabel[tabel['Year'] != 'Grand Total']
        tabel = tabel[tabel['Country'] != 'Grand Total']
        tabel['Year'] = tabel['Year'].astype(float).astype(int)
        tabel['Year'] = pd.to_datetime(tabel['Year'], format='%Y')
        tabel['Year'] = tabel['Year'].dt.year

        # Get the previous year
        latest_year = tabel['Year'].max()
        return tabel[tabel['Year'] == latest_year - 1].sum()['Value']

    def avg_latest_year(data_sheets):
        data_sheets.columns = data_sheets.iloc[0].astype(str)
        data_sheets = data_sheets.iloc[1:]
        data_sheets = data_sheets.dropna(subset=['Negara'])

        tabel = pd.melt(data_sheets, id_vars=['Negara'], var_name='Year', value_name='Value')
        tabel.rename(columns={'Negara': 'Country'}, inplace=True)
        tabel = tabel[tabel['Year'] != 'Grand Total']
        tabel['Year'] = tabel['Year'].astype(float).astype(int)
        tabel['Year'] = pd.to_datetime(tabel['Year'], format='%Y')
        tabel['Year'] = tabel['Year'].dt.year

        # Get the latest year
        latest_year = tabel['Year'].max()
        return tabel[(tabel['Year'] == latest_year) & (tabel['Country'] == 'Grand Total')]['Value'].values[0]

    def avg_prev_year(data_sheets):
        data_sheets.columns = data_sheets.iloc[0].astype(str)
        data_sheets = data_sheets.iloc[1:]
        data_sheets = data_sheets.dropna(subset=['Negara'])

        tabel = pd.melt(data_sheets, id_vars=['Negara'], var_name='Year', value_name='Value')
        tabel.rename(columns={'Negara': 'Country'}, inplace=True)
        tabel = tabel[tabel['Year'] != 'Grand Total']
        tabel['Year'] = tabel['Year'].astype(float).astype(int)
        tabel['Year'] = pd.to_datetime(tabel['Year'], format='%Y')
        tabel['Year'] = tabel['Year'].dt.year

        # Get the previous year
        latest_year = tabel['Year'].max()
        return tabel[(tabel['Year'] == latest_year - 1) & (tabel['Country'] == 'Grand Total')]['Value'].values[0]

    def yoy_transaksi(data_sheets, kolom):
        # Calculate the mean of the 'Transaksi YoY' column
        yoy = data_sheets[kolom].mean()
        return yoy




    # Main Content
    st.title('LCT Infografis')

    nasabah_latest = int(avg_latest_year(nasabah))
    nasabah_previous = int(avg_prev_year(nasabah))

    transaksi_latest = total_latest_year(transaksi)
    transaksi_previous = total_previous_year(transaksi)

    col1, col2 = st.columns(2)

    col1.metric("Total Nasabah LCT (Pelaku Usaha)", 
                f"{nasabah_latest:,}",
                f"{nasabah_latest - nasabah_previous}")
    col2.metric(
        "Total Transaksi LCT",
        "$" + f"{transaksi_latest:,.2f}",  # Formats number with commas and 2 decimal places
        f"{transaksi_latest - transaksi_previous:,.2f}"  # Formats difference similarly
    )

    nasabahGrowth_latest = yoy_transaksi(growthYOY, 'Transaksi YoY')
    transaksiGrowth_latest = yoy_transaksi(growthYOY, 'Nasabah YoY')
    
    col3, col4 = st.columns(2)

    col3.metric(
        "Pertumbuhan nasabah yoy(%)",
        f"{nasabahGrowth_latest:,.2f}",  # Formats number with commas and 2 decimal places
    )
    col4.metric(
        "Pertumbuhan Transaksi yoy(%)",
        f"{transaksiGrowth_latest:,.2f}",  # Formats number with commas and 2 decimal places
    )
else:
    st.warning("Please upload an Excel file to proceed.")
