import streamlit as st
import pandas as pd
import numpy as np

uploaded_file = st.file_uploader("选择一个文件")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)
