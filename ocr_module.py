import io
import re
from PyPDF2 import PdfReader

def extract_invoice_fields_from_pdf_bytes(pdf_bytes: bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        txt = page.extract_text()
        if txt:
            text += txt

    result = {"Invoice No": "", "Date": "", "GSTIN": "", "Amount": ""}

    # find GSTIN
    gst_match = re.search(r'\d{2}[A-Z]{5}\d{4}[A-Z]\dZ\d', text)
    if gst_match:
        result["GSTIN"] = gst_match.group()

    # find Invoice No
    inv_match = re.search(r'Invoice\s*No\.?\s*[:\-]?\s*([A-Z0-9\-\/]+)', text, re.I)
    if inv_match:
        result["Invoice No"] = inv_match.group(1)

    # find Date
    date_match = re.search(r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}', text)
    if date_match:
        result["Date"] = date_match.group()

    # find Amount
    amt_match = re.search(r'(?:Total|Amount)\s*[:\-]?\s*₹?\s*([0-9,]+)', text, re.I)
    if amt_match:
        result["Amount"] = amt_match.group(1)

    return result
