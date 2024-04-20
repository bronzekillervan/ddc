import streamlit as st
import pandas as pd
import pydeck as pdk

st.title('路线绘制应用')

# 文件上传器
uploaded_file = st.file_uploader("请选择表格文件", type=['csv', 'xlsx'])

def draw_route(df):
    # 筛选出有有效经纬度的行
    valid_routes = df.dropna(subset=['pickup_lat', 'pickup_lng', 'receiving_lat', 'receiving_lng'])

    # 创建路径数据
    routes = [
        {
            "start": [row['pickup_lng'], row['pickup_lat']],
            "end": [row['receiving_lng'], row['receiving_lat']],
        } for index, row in valid_routes.iterrows()
    ]

    # 设置地图图层
    layer = pdk.Layer(
        type="PathLayer",
        data=routes,
        pickable=True,
        get_path="data",
        width_scale=20,
        width_min_pixels=2,
        get_color="[255, 140, 0]",
        width_units="pixels",
    )

    # 设置地图视图
    view_state = pdk.ViewState(
        latitude=valid_routes['pickup_lat'].mean(),
        longitude=valid_routes['pickup_lng'].mean(),
        zoom=10
    )

    # 渲染地图
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

if uploaded_file is not None:
    # 根据文件类型读取数据
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 检查是否包含必要的列
    if all(col in df.columns for col in ['pickup_lat', 'pickup_lng', 'receiving_lat', 'receiving_lng']):
        draw_route(df)
    else:
        st.error('表格中没有找到必要的列。需要有 "pickup_lat", "pickup_lng", "receiving_lat", 和 "receiving_lng"。')
else:
    st.info('请上传文件以绘制路线。')


