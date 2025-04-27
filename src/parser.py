# create function get_data_from_pdf that will read and extract raw text
import PyPDF2

def get_data_from_pdf(path):
    """Extracts and returns all text from a PDF file."""
    text = ""
    try:
        with open(path, 'rb') as pdf_file:  
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""  
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text


# create function align_content
# Split the raw text line by line, it should align as it appears in the PDF.

def align_content(raw_text):
    lines = raw_text.split('\n')
    aligned = [line.strip() for line in lines if line.strip()]
    return aligned
