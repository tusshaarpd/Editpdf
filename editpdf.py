import streamlit as st
import pdfplumber
from fpdf import FPDF
import os

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def create_pdf(text, output_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for line in text.split("\n"):
        try:
            pdf.cell(200, 10, txt=line.encode("latin-1", "replace").decode("latin-1"), ln=True, align='L')
        except UnicodeEncodeError:
            pdf.cell(200, 10, txt="(Unicode Error: Unable to display)", ln=True, align='L')
    
    pdf.output(output_path, "F")

def main():
    st.title("Editable PDF Application")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Extracting text..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
            edited_text = st.text_area("Edit the extracted text", extracted_text, height=400)
            
            if st.button("Download Edited PDF"):
                output_path = "edited_output.pdf"
                create_pdf(edited_text, output_path)
                with open(output_path, "rb") as f:
                    st.download_button("Download PDF", f, file_name="edited_document.pdf", mime="application/pdf")
                os.remove(output_path)

if __name__ == "__main__":
    main()
