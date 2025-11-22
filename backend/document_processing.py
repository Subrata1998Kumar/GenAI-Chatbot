import os
import PyPDF2
import pdfplumber
import docx

class DocumentProcessor:
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        text = ""
        # with open(file_path, 'rb') as file:
        with pdfplumber.open(file_path) as reader:
            # reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        text = ""
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.txt':
            return DocumentProcessor.extract_text_from_txt(file_path)
        elif ext == '.pdf':
            return DocumentProcessor.extract_text_from_pdf(file_path)
        elif ext == '.docx':
            return DocumentProcessor.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported formats are .txt, .pdf, .docx")

if __name__ == "__main__":
    pdf_path = r"./data/sample.pdf"
    doc_path = r"./data/sample.docx"
    txt_path = r"./data/sample.txt"
    pdf_text = DocumentProcessor.extract_text(pdf_path)
    doc_text = DocumentProcessor.extract_text(doc_path)
    txt_text = DocumentProcessor.extract_text(txt_path)
    print(pdf_text)
    print("--"*50)
    print(doc_text)
    print("--"*50)
    print(txt_text)