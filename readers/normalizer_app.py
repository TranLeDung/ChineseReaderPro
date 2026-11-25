import io

import streamlit as st

from services.docx_normalizer import (
    normalize_docx
)

st.title(
    "DOCX Normalizer"
)

uploaded_file = st.file_uploader(
    "Chọn DOCX",
    type=["docx"]
)

if uploaded_file:

    df = normalize_docx(
        uploaded_file
    )

    st.dataframe(df)

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Lesson"
        )

    st.download_button(
        "⬇ Tải Excel chuẩn hóa",
        data=output.getvalue(),
        file_name="normalized.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )