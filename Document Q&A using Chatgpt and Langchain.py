
import streamlit as st
import openai
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS,ElasticVectorSearch, Pinecone, Weaviate
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from PIL import Image
import pytesseract
import cv2
import PyPDF2
import pandas as pd
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ManujKumarJoshi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
openai.api_key = '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'

# Streamlit App
st.title("Get Answers from your file!!")

# Upload File
file = st.file_uploader("Upload a PDF, Image, or Excel file", type=["pdf", "png", "jpg", "jpeg", "xlsx"])
text = 'Welcome to Celebal Technologies!!'
if file is not None:
    file_type = file.type
    # If PDF file
    #### Redad text from PDF
    if file_type == 'application/pdf':
        pdf_reader = PyPDF2.PdfReader(file)
        # Get the total number of pages in the PDF
        num_pages = len(pdf_reader.pages)  ###pdf_reader.numPages  
        # Add a selectbox to select a page to display
        page_number = st.selectbox("Select a page to display", list(range(1, num_pages + 1)))
        # Extract the text from the selected page
        page =   pdf_reader.pages[page_number-1] 
        text =   page.extract_text()  
        

    # If Image file
    ### Read tetx from Image
    elif file_type == 'image/png' or file_type == 'image/jpg' or file_type == 'image/jpeg':
        st.write("Reading text from Image file...")
        image = cv2.imread(file.name)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)

    # If Excel file
    elif file_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        st.write("Reading data from Excel file...")
        excel_df = pd.read_excel(file)
        text = excel_df.to_string(header=False, index=False)

    else:
        st.write("Unsupported file type. Please upload a PDF, Image, or Excel file.")

# Define the Streamlit app
def question(text):
    os.environ["OPENAI_API_KEY"] = "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"
    
    raw_text = text

    text_splitter = CharacterTextSplitter(        
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap  = 200,
        length_function = len,
    )
    texts = text_splitter.split_text(raw_text)
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)
    chain = load_qa_chain(OpenAI(), chain_type="stuff")

    user_input = st.text_input("Enter Question from your file!!",'Enter some text!!')
    query = user_input
    docs = docsearch.similarity_search(query)
    st.write(chain.run(input_documents=docs, question=query))

question(text)