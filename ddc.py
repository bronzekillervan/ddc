import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("请选择一个文件")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    if len(data.columns) > 1:
        # 创建一个临时的DataFrame来显示第三列
        third_column_data = data.iloc[:, 1].to_frame()
        third_column_data['index'] = third_column_data.index
        # 展示第三列的数据
        st.dataframe(third_column_data)

        # 定义用户选择行的交互
        selected_indices = st.multiselect("选择要查看详情的index", third_column_data['index'])
        for selected_index in selected_indices:
            st.write(data.loc[selected_index, :])
else:
    st.write("请上传CSV文件。")

