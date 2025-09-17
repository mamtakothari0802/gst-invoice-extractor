# streamlit_app.py
import streamlit as st
import pandas as pd
from ocr_module import extract_invoice_fields_from_pdf_bytes

st.set_page_config(page_title="GST Invoice Extractor (Batch)", layout="centered")
st.title("GST Invoice Extractor — Batch Upload")

st.markdown("Upload one or more **digital PDF invoices**. The app will extract Invoice No, Date, GSTIN, and Amount for each file and give a single CSV with all results.")

uploaded_files = st.file_uploader("Upload invoice PDFs (you can select multiple)", type=["pdf"], accept_multiple_files=True)

if not uploaded_files:
    st.info("Upload 1 or more PDF files to extract data.")
else:
    rows = []
    errors = []
    for uploaded in uploaded_files:
        try:
            file_bytes = uploaded.read()
            fields = extract_invoice_fields_from_pdf_bytes(file_bytes)
            # Keep track of source filename
            fields["source_file"] = uploaded.name
            rows.append(fields)
        except Exception as e:
            errors.append({"file": uploaded.name, "error": str(e)})

    if rows:
        df = pd.DataFrame(rows)
        st.subheader("Extracted fields from all files")
        st.table(df)
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download combined CSV", csv_bytes, file_name="all_invoices_extracted.csv")
    else:
        st.warning("No data extracted from uploaded files.")

    if errors:
        st.subheader("Files with problems")
        err_df = pd.DataFrame(errors)
        st.table(err_df)
