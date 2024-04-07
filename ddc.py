import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("请选择一个文件")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    # 假设您的数据有足够的列
    if len(data.columns) > 1:
        # 只显示第二列（即第三列，因为索引从0开始）
        third_column_data = data.iloc[:, 1].to_frame()
        third_column_data['index'] = third_column_data.index
        
        # 展示第三列的数据和一个选择框来选择行
        st.dataframe(third_column_data)
        selected_indices = st.multiselect("select the index", third_column_data['index'])

        # 对选中的每一行，显示行的内容和操作按钮
        for selected_index in selected_indices:
            st.write(data.loc[selected_index, :])
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('edit', key=f'edit_{selected_index}'):
                    # 编辑逻辑
                    st.session_state['edit_row_index'] = selected_index
                    st.session_state['edit'] = True
            with col2:
                if st.button('delet', key=f'del_{selected_index}'):
                    # 删除逻辑
                    data = data.drop(index=selected_index)
                    data.reset_index(drop=True, inplace=True)
            with col3:
                if st.button('add', key=f'add_{selected_index}'):
                    # 添加逻辑
                    st.session_state['add'] = True
        
        # 添加或编辑数据的表单
        if st.session_state.get('add', False) or st.session_state.get('edit', False):
            with st.form(key='edit_add_form'):
                new_data = {}
                for column in data.columns:
                    new_data[column] = st.text_input(f"input {column}", 
                                value=data.loc[st.session_state['edit_row_index'], column] if st.session_state.get('edit', False) else "")
                submit_button = st.form_submit_button(label='submit')
                if submit_button:
                    if st.session_state.get('edit', False):
                        data.loc[st.session_state['edit_row_index']] = pd.Series(new_data)
                    else:
                        data = data.append(new_data, ignore_index=True)
                    # 重置状态
                    st.session_state['add'] = False
                    st.session_state['edit'] = False
                    st.session_state['edit_row_index'] = None
        # 显示操作后的数据
        st.write(data)
else:
    st.write("请上传CSV文件。")
