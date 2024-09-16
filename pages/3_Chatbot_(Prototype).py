import os
import streamlit as st
import translators as ts

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import PyPDFLoader

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


os.environ["GOOGLE_API_KEY"] = "AIzaSyCCU2RqgAErWjYupSAAZ-KrIfYenyTS7CA"

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


# Function to clear chat history
def clear_history():
    if 'history' in st.session_state:
        del st.session_state['history']

# Streamlit app
st.title('Chat with Document')  # title in our web page

# File uploader
uploaded_file = st.file_uploader('Upload file:', type=['pdf', 'docx', 'txt'])
add_file = st.button('Add File', on_click=clear_history)

if uploaded_file and add_file:
    with st.spinner('Reading, chunking and embedding file...'):
        bytes_data = uploaded_file.read()
        file_name = os.path.join('./', uploaded_file.name)
        with open(file_name,'wb') as f:
            f.write(bytes_data)

    name, extension = os.path.splitext(file_name)

    if extension == '.pdf':
        loader = PyPDFLoader(file_name)
    elif extension == '.docx':
        loader = Docx2txtLoader(file_name)
    elif extension == '.txt':
        loader = TextLoader(file_name)
    else:
        st.write('Document format is not supported!') 
        

    documents = loader.load()
    
    # Split document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    # Embed document chunks
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(chunks, embeddings)
    
    # Initialize llm instance
    llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
    # other params...
  )


    retriever = vector_store.as_retriever()
    crc = ConversationalRetrievalChain.from_llm(llm, retriever)
    st.session_state.crc = crc
    
    # Success message
    st.success('File uploaded, chunked and embedded successfully')

else:
    st.write('No file uploaded')

# Get question from user input
question = st.text_input('Input your question')

if question:
    if 'crc' in st.session_state:
        crc = st.session_state.crc
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    # Get response from CRC
    response = crc.run({
        'question': ts.translate_text(question,
                                      translator="google",
                                      from_language="id",
                                      to_language="en"),
        'chat_history': st.session_state['history']
    })
    
    # Save chat history
    st.session_state['history'].append((
        ts.translate_text(question,
                          translator="google",
                          from_language="id",
                          to_language="en"),
        response
    ))
    
    # Display response
    st.write(ts.translate_text(response,
                          translator="google",
                          from_language="en",
                          to_language="id"))


