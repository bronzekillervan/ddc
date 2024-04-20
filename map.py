import streamlit as st
import pandas as pd
import pydeck as pdk

# 设置页面标题
st.title('立体弧线路线绘制应用')

# GitHub文件的直接链接（确保链接是指向原始内容的）
file_url = 'https://raw.githubusercontent.com/bronzekillervan/ddc/main/cdw_csv_sample.csv'

def draw_routes(df):
    # 仅选择包含有效经纬度数据的行
    valid_routes = df.dropna(subset=['pickup_lat', 'pickup_lng', 'receiving_lat', 'receiving_lng'])

    # 创建包含所有运输信息的路径数据
    routes = [
        {
            "from_coordinates": [row['pickup_lng'], row['pickup_lat']],
            "to_coordinates": [row['receiving_lng'], row['receiving_lat']],
            # 添加详细信息到Tooltip，并为每个项目换行
            "info": ("<b>Type of Debris:</b> {type_debris}<br>"
                     "<b>Waste Quantity:</b> {waste_quantity}<br>"
                     "<b>Pickup Name:</b> {pickup_name}<br>"
                     "<b>Pickup Address:</b> {pickup_address}<br>"
                     "<b>Generator Name:</b> {generator_name}<br>"
                     "<b>Generator Address:</b> {generator_address}").format(
                         type_debris=row['type_debris'],
                         waste_quantity=row['waste_quantity'],
                         pickup_name=row['pickup_name'],
                         pickup_address=row['pickup_address'],
                         generator_name=row['generator_name'],
                         generator_address=row['generator_address']
                     )
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
        get_tilt=15,
        get_color=[255, 182, 193, 255],  # 设置为粉色
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
        "html": "{info}",  # 仅使用info字段，因为它已经包含HTML格式的数据
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
        map_style='mapbox://styles/mapbox/light-v10'
    ))

# 从GitHub URL读取CSV文件
df = pd.read_csv(file_url)

# 检查必要的列是否存在并开始绘制路线
if {'type_debris', 'waste_quantity', 'pickup_lat', 'pickup_lng', 'receiving_lat', 'receiving_lng', 'pickup_name', 'pickup_address', 'generator_name', 'generator_address'}.issubset(df.columns):
    draw_routes(df)
else:
    st.error('表格中没有找到必要的列。')


