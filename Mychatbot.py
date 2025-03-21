import streamlit as st
import csv
import json
import os
import fitz  # PyMuPDF
import pdfplumber
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Configure Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize Groq AI Model
from langchain_groq import ChatGroq

lln = ChatGroq(model="llama3-70b-8192", api_key="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")

# CSV File Path to store chat history
csv_filename = "chat_history.csv"


def extract_text_from_pdf(pdf_path):
    """Extract text from structured and unstructured PDFs."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip() if text else "No text extracted."


# Streamlit navigation
page = st.sidebar.radio("Select a Page", ["AI Chat", "PDF Extraction"])

if page == "AI Chat":
    st.title("🤖 AI Chatbot using Groq (Llama3)")
    st.write("Type your message below and get responses in real time!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Enter your prompt:", "")
    if st.button("Send"):
        if user_input:
            response = lln.invoke(user_input)
            response_text = response.content if hasattr(response, "content") else str(response)
            st.session_state.chat_history.append({"prompt": user_input, "response": response_text})
            with open(csv_filename, "a", newline="", encoding="utf-8") as file:
                csv.writer(file).writerow([user_input, response_text])
            st.json({"prompt": user_input, "response": response_text})

    st.subheader("Chat History")
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['prompt']}")
        st.write(f"**AI:** {chat['response']}")
        st.write("---")

elif page == "PDF Extraction":
    st.title("📄 PDF Text Extraction")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Process PDF"):
            file_path = f"temp_{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            extracted_text = extract_text_from_pdf(file_path)
            os.remove(file_path)  # Cleanup temp file
            st.text_area("Extracted Text", extracted_text, height=300)

            # Provide download link
            st.download_button("Download Extracted Text", extracted_text, file_name="extracted_text.txt")
