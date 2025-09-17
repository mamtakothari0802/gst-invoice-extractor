import streamlit as st
import pandas as pd
from ocr_module import extract_invoice_fields_from_pdf_bytes

st.title("GST Invoice Extractor")

uploaded = st.file_uploader("Upload your Invoice PDF", type=["pdf"])

if uploaded:
    bytes_data = uploaded.read()
    fields = extract_invoice_fields_from_pdf_bytes(bytes_data)
    df = pd.DataFrame([fields])
    st.write("Here are the details I found:")
    st.table(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download as CSV", csv, "invoice_data.csv")
