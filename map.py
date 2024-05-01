import streamlit as st
import pandas as pd
import pydeck as pdk

# 设置页面标题
st.title('DDC Mapping Program')

# 加载数据
file_url = 'https://raw.githubusercontent.com/TianyiWuNYU/test/main/data/cdw_sample.csv'
df = pd.read_csv(file_url)

# 用户界面允许选择type_debris
unique_debris_types = df['type_debris'].unique()
selected_debris = st.selectbox('Select Type of Debris:', unique_debris_types)

# 用户界面允许选择pickup_address
unique_pickup_addresses = df['pickup_address'].unique()
selected_pickup_address = st.selectbox('Select Pickup Address:', unique_pickup_addresses)

# 用户界面允许选择receiving_address
unique_receiving_addresses = df['receiving_address'].unique()
selected_receiving_address = st.selectbox('Select Receiving Address:', unique_receiving_addresses)

# 过滤数据
filtered_data = df[
    (df['type_debris'] == selected_debris) &
    (df['pickup_address'] == selected_pickup_address) &
    (df['receiving_address'] == selected_receiving_address)
]

def draw_routes(filtered_data):
    if not filtered_data.empty:
        routes = [
            {
                "from_coordinates": [row['pickup_lng'], row['pickup_lat']],
                "to_coordinates": [row['receiving_lng'], row['receiving_lat']],
                "info": f"Type of Debris: {row['type_debris']}<br>"
                        f"Waste Quantity: {row['waste_quantity']}<br>"
                        f"Pickup Name: {row['pickup_name']}<br>"
                        f"Pickup Address: {row['pickup_address']}<br>"
                        f"Generator Name: {row['generator_name']}<br>"
                        f"Generator Address: {row['generator_address']}"
            }
            for _, row in filtered_data.iterrows()
        ]

        layer = pdk.Layer(
            "ArcLayer",
            routes,
            get_source_position="from_coordinates",
            get_target_position="to_coordinates",
            get_width=5,
            get_tilt=15,
            get_color=[135, 206, 235, 255],
            pickable=True,
            auto_highlight=True,
        )

        view_state = pdk.ViewState(
            latitude=filtered_data['pickup_lat'].mean(),
            longitude=filtered_data['pickup_lng'].mean(),
            zoom=6
        )

        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style='mapbox://styles/mapbox/light-v10'
        ))
    else:
        st.error('No routes found for the selected options.')

# 绘制路线图
draw_routes(filtered_data)



