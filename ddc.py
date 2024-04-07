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
        selected_indices = st.multiselect("select the index", third_column_data['index'])

        for selected_index in selected_indices:
            st.write(data.loc[selected_index, :])
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('edit', key=f'edit_{selected_index}'):
                    st.session_state['edit_row_index'] = selected_index
                    st.session_state['edit'] = True
            with col2:
                if st.button('delete', key=f'del_{selected_index}'):
                    # 直接在session state中操作删除
                    st.session_state.data = st.session_state.data.drop(index=selected_index)
                    st.session_state.data.reset_index(drop=True, inplace=True)
            with col3:
                if st.button('add', key=f'add_{selected_index}'):
                    st.session_state['add'] = True
        
        if st.session_state.get('add', False) or st.session_state.get('edit', False):
            with st.form(key='edit_add_form'):
                new_data = {}
                for column in data.columns:
                    default_value = data.loc[st.session_state['edit_row_index'], column] if st.session_state.get('edit', False) else ""
                    new_data[column] = st.text_input(f"input {column}", value=default_value)
                submit_button = st.form_submit_button(label='submit')
                if submit_button:
                    if st.session_state.get('edit', False):
                        # 直接在session state中操作编辑
                        st.session_state.data.loc[st.session_state['edit_row_index']] = pd.Series(new_data)
                    elif st.session_state.get('add', False):
                        # 在session state中操作添加
                        # 创建一个新的DataFrame来添加数据
                        new_row = pd.DataFrame([new_data], columns=data.columns)
                        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
                    # 重置添加和编辑的标志
                    st.session_state['add'] = False
                    st.session_state['edit'] = False
                    st.session_state['edit_row_index'] = None

        # 最后，确保展示的是session state中的最新数据
        st.write(st.session_state.data)
else:
    st.write("请上传CSV文件。")

