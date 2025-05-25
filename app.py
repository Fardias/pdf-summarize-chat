import streamlit as st
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from pypdf import PdfReader
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Set page config
st.set_page_config(page_title="PDF Chatbot", page_icon="📚")

# Add custom CSS
st.markdown("""
<style>
    .stTextInput input:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2) !important;
    }
    .stTextInput input {
        border-color: #d1d5db !important;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("📚 PDF Chatbot")
st.write("Upload a PDF file and ask questions about its content!")

# Initialize session state for summaries
if 'summaries' not in st.session_state:
    st.session_state.summaries = None

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    try:
        # Read PDF
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Only generate summaries if they haven't been generated yet
        if st.session_state.summaries is None:
            # Summarize the content in English
            with st.spinner("Summarizing content..."):
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
                english_prompt = f"Please provide a concise summary of the following text in English:\n\n{text}\n\nSummary:" 
                english_summary = llm.invoke(english_prompt)
                
            # Summarize the content in Indonesian
            with st.spinner("Menghasilkan ringkasan dalam Bahasa Indonesia..."):
                indonesian_prompt = f"Tolong berikan ringkasan yang singkat dari teks berikut dalam Bahasa Indonesia:\n\n{text}\n\nRingkasan:" 
                indonesian_summary = llm.invoke(indonesian_prompt)
                
            # Store both summaries in session state
            st.session_state.summaries = {
                'english': english_summary.content,
                'indonesian': indonesian_summary.content
            }

        # Display stored summaries
        if st.session_state.summaries:
            st.write("📝 Summary (English):", st.session_state.summaries['english'])
            st.write("📝 Ringkasan (Bahasa Indonesia):", st.session_state.summaries['indonesian'])

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # Create embeddings and vector store
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(chunks, embeddings)

        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0),
            chain_type="stuff",
            retriever=vector_store.as_retriever()
        )

        # Chat interface
        st.write("Ask questions about the PDF content:")
        question = st.text_input("Your question:")

        if question:
            with st.spinner("Thinking..."):
                # Get answer
                answer = qa_chain.invoke({"query": question})
                st.write("Answer:", answer["result"])
    except Exception as e:
        if "API key" in str(e):
            st.error("Error: API key Gemini tidak ditemukan. Silakan tambahkan GOOGLE_API_KEY di file .env")
        else:
            st.error(f"Terjadi kesalahan: {str(e)}")
else:
    st.info("Please upload a PDF file to begin.") 