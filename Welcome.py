import streamlit as st

# Set the page configuration at the very beginning
st.set_page_config(
    page_title="Hello",
    page_icon="Landing Page",
)

# Correct file path for the CSS file
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

st.write("# LCT Dashboard ")

# Initialize session state for the uploaded file
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

# File uploader
uploaded_file = st.file_uploader('Upload File Untuk Visualisasi Dan Chatbot:', type=['xlsx'])

# Store the uploaded file in session state
if uploaded_file is not None:
    st.session_state['uploaded_file'] = uploaded_file
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

# Access the file across pages
if st.session_state['uploaded_file']:
    st.write(f"Using the file: {st.session_state['uploaded_file'].name}")
    # Add logic to use the file here
else:
    st.write("No file uploaded.")

# Optional: Button to clear the uploaded file from session state
if st.button('Clear File'):
    del st.session_state['uploaded_file']
    st.success("File cleared.")

st.markdown(
    """
    Dashboard ini  dirancang untuk memberikan informasi terkini dan komprehensif mengenai Program Local Currency Settlement (LCS) yang diinisiasi oleh Bank Indonesia.

    Program LCS bertujuan untuk memfasilitasi transaksi perdagangan internasional menggunakan mata uang lokal, yang dapat memperkuat stabilitas ekonomi dan mengurangi ketergantungan pada mata uang asing. Di dashboard ini, Anda dapat memantau berbagai metrik dan indikator kunci terkait pelaksanaan program ini, termasuk volume transaksi, partisipasi institusi, dan dampak ekonomi.

    Fitur Utama:

    Visualisasi Data: Akses grafik dan tabel yang menggambarkan data transaksi LCS secara real-time.
    Analisis Tren: Pantau perkembangan dan tren utama dari waktu ke waktu.
    Interaktif dan Responsif: Jelajahi data melalui antarmuka yang user-friendly dan responsif.

    Anda punya pertanyaan? coba konsultasikan dengan chatbot kami 🤖


    """
)
