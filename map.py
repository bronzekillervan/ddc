import streamlit as st
import pandas as pd
import pydeck as pdk

st.title('立体弧线路线绘制应用')

# 文件上传器
uploaded_file = st.file_uploader("请选择表格文件", type=['csv', 'xlsx'])

def draw_routes(df):
    # 仅选择包含有效经纬度数据的行
    valid_routes = df.dropna(subset=['pickup_lat', 'pickup_lng', 'receiving_lat', 'receiving_lng'])

    # 创建包含所有运输信息的路径数据
    routes = [
        {
            "from_coordinates": [row['pickup_lng'], row['pickup_lat']],
            "to_coordinates": [row['receiving_lng'], row['receiving_lat']],
            # 添加详细信息到Tooltip
            "info": f"Type of Debris: {row['type_debris']}, Waste Quantity: {row['waste_quantity']}, "
                    f"Pickup Name: {row['pickup_name']}, Pickup Address: {row['pickup_address']}, "
                    f"Generator Name: {row['generator_name']}, Generator Address: {row['generator_address']}"
        }
        for _, row in valid_routes.iterrows()
    ]

    # 创建pydeck的ArcLayer
    layer = pdk.Layer(
        "ArcLayer",
        routes,
        get_source_position="from_coordinates",
        get_target_position="to_coordinates",
        get_width=5,
        get_tilt=15,  # 控制弧线的倾斜度
        get_color=[255, 182, 193,255],  # 粉色弧线的RGB颜色代码
        pickable=True,
        auto_highlight=True,
    )

    # 设置初始视图状态
    view_state = pdk.ViewState(
        latitude=valid_routes['pickup_lat'].mean(),
        longitude=valid_routes['pickup_lng'].mean(),
        zoom=6
    )

    # 定义Tooltip
    tooltip = {
        "html": "<b>运输信息:</b> {info}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    # 用pydeck渲染地图
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style='mapbox://styles/mapbox/light-v10'  # 使用Mapbox的浅色地图样式
    ))

if uploaded_file is not None:
    # 根据文件类型读取数据
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    # 检查必要的列是否存在
    if {'type_debris', 'waste_quantity', 'pickup_lat', 'pickup_lng', 'receiving_lat', 'receiving_lng', 'pickup_name', 'pickup_address', 'generator_name', 'generator_address'}.issubset(df.columns):
        draw_routes(df)
    else:
        st.error('表格中没有找到必要的列。')
else:
    st.info('请上传文件以绘制路线。')





