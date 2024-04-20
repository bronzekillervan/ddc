import streamlit as st
import pandas as pd

def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    return data

uploaded_file = st.file_uploader("请选择一个文件")
if uploaded_file is not None:
    # 确保会话状态中的数据是最新的
    if 'data' not in st.session_state or st.session_state.uploaded_file_name != uploaded_file.name:
        st.session_state.data = load_data(uploaded_file)
        st.session_state.uploaded_file_name = uploaded_file.name

    data = st.session_state.data
    
    if len(data.columns) > 1:
        third_column_data = data.iloc[:, 1].to_frame()
        third_column_data['index'] = third_column_data.index
        st.dataframe(third_column_data)
        
        # 如果想要对选定行进行任何额外的操作，可以在这里添加
        selected_indices = st.multiselect("选择行索引", third_column_data['index'])
        for selected_index in selected_indices:
            st.write(data.loc[selected_index, :])

        # 展示更新后的数据
        st.write(st.session_state.data)
else:
    st.write("请上传CSV文件。")

