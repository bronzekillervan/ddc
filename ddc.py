import streamlit as st
import pandas as pd

def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    return data

uploaded_file = st.file_uploader("Please upload a file")
if uploaded_file is not None:
    if 'data' not in st.session_state or st.session_state.uploaded_file_name != uploaded_file.name:
        st.session_state.data = load_data(uploaded_file)
        st.session_state.uploaded_file_name = uploaded_file.name

    data = st.session_state.data
    
    if len(data.columns) > 1:
        third_column_data = data.iloc[:, 1].to_frame()
        third_column_data['index'] = third_column_data.index
        st.dataframe(third_column_data)
        
        selected_indices = st.multiselect("select an index", third_column_data['index'])
        for selected_index in selected_indices:
            st.write(data.loc[selected_index, :])
        st.write(st.session_state.data)
else:
    st.write("Please upload a file")

