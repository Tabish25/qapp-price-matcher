import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Qapp Subscription Merger")

uploaded_file = st.file_uploader(
    "Upload Qapp File",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    original_rows = len(df)

    # Merge entire subscription line
    merged_df = (
        df.groupby(
            ["Subscription ID", "Code"],
            as_index=False
        )
        .first()
    )

    merged_rows = len(merged_df)

    st.success("Merge completed")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Original Rows",
        original_rows
    )

    col2.metric(
        "Merged Rows",
        merged_rows
    )

    col3.metric(
        "Duplicates Removed",
        original_rows - merged_rows
    )

    st.dataframe(merged_df)

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:
        merged_df.to_excel(
            writer,
            index=False,
            sheet_name="Merged"
        )

    st.download_button(
        "Download Merged File",
        output.getvalue(),
        "Merged_Subscriptions.xlsx"
    )
