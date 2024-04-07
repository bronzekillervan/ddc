import streamlit as st
import pandas as pd

# 定义加载数据的函数
def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    return data

# 显示初始页面，包含图片和继续按钮
if 'init' not in st.session_state:
    st.session_state['init'] = True  # 初始状态为True，显示欢迎页面

if st.session_state['init']:
    # 使用GitHub图片的URL（确保URL是公开的）
    github_image_url = 'https://github.com/bronzekillervan/ddc/blob/main/203d909c2f8e428ec1828d27b0cca0b.png?raw=true'
    st.image(github_image_url, caption='孩子们，我回来了')
    if st.button('牢大，想你了！！'):
        st.session_state['init'] = False  # 用户点击后，切换状态

# 当用户点击继续后，显示文件上传器和数据操作界面
if not st.session_state['init']:
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
            selected_indices = st.multiselect("选择行索引", third_column_data['index'])

            for selected_index in selected_indices:
                st.write(data.loc[selected_index, :])
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button('编辑', key=f'edit_{selected_index}'):
                        st.session_state['edit_row_index'] = selected_index
                        st.session_state['edit'] = True
                with col2:
                    if st.button('删除', key=f'del_{selected_index}'):
                        st.session_state.data = st.session_state.data.drop(index=selected_index)
                        st.session_state.data.reset_index(drop=True, inplace=True)
                with col3:
                    if st.button('添加', key=f'add_{selected_index}'):
                        st.session_state['add'] = True
            
            if st.session_state.get('add', False) or st.session_state.get('edit', False):
                with st.form(key='edit_add_form'):
                    new_data = {}
                    for column in data.columns:
                        default_value = data.loc[st.session_state['edit_row_index'], column] if st.session_state.get('edit', False) else ""
                        new_data[column] = st.text_input(f"输入 {column}", value=default_value)
                    submit_button = st.form_submit_button(label='提交')
                    if submit_button:
                        if st.session_state.get('edit', False):
                            st.session_state.data.loc[st.session_state['edit_row_index']] = pd.Series(new_data)
                        elif st.session_state.get('add', False):
                            new_row = pd.DataFrame([new_data], columns=data.columns)
                            st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
                        st.session_state['add'] = False
                        st.session_state['edit'] = False
                        st.session_state['edit_row_index'] = None

            st.write(st.session_state.data)
    else:
        st.write("请上传CSV文件。")
