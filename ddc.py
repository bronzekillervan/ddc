import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("请选择一个文件")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    if len(data.columns) > 2:
        # 创建一个包含第三列所有数据的临时DataFrame
        third_column_data = pd.DataFrame(data.iloc[:, 2])

        # 创建一个新的列，用于点击后展开详细信息
        third_column_data['详情'] = third_column_data.apply(lambda row: "点击查看", axis=1)

        # 使用st.dataframe显示第三列以及新加的"详情"列
        st.dataframe(third_column_data)

        # 获取用户点击的行
        clicked = st.session_state.get('clicked')
        if clicked is not None:
            # 使用st.expander展示被点击行的详细数据
            with st.expander("详细信息"):
                st.table(data.iloc[clicked, :])
        
        # 点击事件的回调函数
        def on_click(index):
            if st.session_state.clicked == index:
                # 如果点击的是同一行，则收起详细信息
                st.session_state.clicked = None
            else:
                # 显示新点击的行的详细信息
                st.session_state.clicked = index

        # 为第三列的每个元素添加点击事件
        for index, _ in third_column_data.iterrows():
            key = f"button_{index}"
            if key not in st.session_state:
                st.session_state[key] = False  # 初始化按钮的状态

            # 创建一个透明的按钮，覆盖在每个单元格上
            st.button("", key=key, on_click=on_click, args=(index,))
else:
    st.write("请上传CSV文件。")
