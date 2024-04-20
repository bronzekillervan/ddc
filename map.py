import streamlit as st
import pandas as pd
import pydeck as pdk

st.title('路线绘制应用')

# 文件上传器
uploaded_file = st.file_uploader("请选择表格文件", type=['csv', 'xlsx'])

def draw_routes(df):
    # 仅选择包含有效经纬度数据的行
    valid_routes = df.dropna(subset=['pickup_lat', 'pickup_lng', 'receiving_lat', 'receiving_lng'])

    # 创建路径数据，每一行是一个字典，包含起点和终点的经纬度坐标
    routes = [
        {"coordinates": [[row['pickup_lng'], row['pickup_lat']], 
                         [row['receiving_lng'], row['receiving_lat']]]}
        for _, row in valid_routes.iterrows()
    ]

    # 创建pydeck的PathLayer
    layer = pdk.Layer(
        "PathLayer",
        routes,
        get_path="coordinates",
        get_width=5,
        get_color=[255, 140, 0],
        pickable=True,
        width_scale=10
    )

    # 设置初始视图状态
    view_state = pdk.ViewState(
        latitude=valid_routes['pickup_lat'].mean(),
        longitude=valid_routes['pickup_lng'].mean(),
        zoom=6
    )

    # 用pydeck渲染地图
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    # 检查必要的列是否存在
    if all(col in df.columns for col in ['pickup_lat', 'pickup_lng', 'receiving_lat', 'receiving_lng']):
        draw_routes(df)
    else:
        st.error('表格中没有找到必要的列。')
else:
    st.info('请上传文件以绘制路线。')




