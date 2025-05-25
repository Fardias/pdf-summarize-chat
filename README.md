# PDF Chatbot with LangChain and OpenAI

This is a Streamlit application that allows you to chat with your PDF documents using OpenAI's language models and LangChain.

## Features

- Upload PDF files
- Ask questions about the PDF content
- Get AI-powered answers based on the document content

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)
3. Upload a PDF file using the file uploader
4. Ask questions about the PDF content in the text input field
5. Get AI-powered answers based on the document content

## Requirements

- Python 3.8 or higher
- OpenAI API key
- Internet connection for API calls

## Note

Make sure to keep your OpenAI API key secure and never share it publicly. 