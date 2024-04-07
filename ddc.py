import streamlit as st
import pandas as pd
import numpy as np

uploaded_file = st.file_uploader("选择一个文件")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    if len(data.columns) >= 3:
        third_column_data = data.iloc[:, 2]
        st.write(third_column_data)
        placeholder = st.empty()
        for index, value in third_column_data.items():
            if st.button(f"{value}", key=index):
                placeholder.write(data.iloc[index, :])
else:
    st.write("请上传CSV文件。")
