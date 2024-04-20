import streamlit as st
import pandas as pd
import pydeck as pdk

# 设置页面标题
st.title('DDC Mapping program')

file_url = 'https://raw.githubusercontent.com/bronzekillervan/ddc/main/cdw_csv_sample.csv'

def draw_routes(df):
    valid_routes = df.dropna(subset=['pickup_lat', 'pickup_lng', 'receiving_lat', 'receiving_lng'])

    routes = [
        {
            "from_coordinates": [row['pickup_lng'], row['pickup_lat']],
            "to_coordinates": [row['receiving_lng'], row['receiving_lat']],
            "info": f"Type of Debris: {row['type_debris']}, Waste Quantity: {row['waste_quantity']}, "
                    f"Pickup Name: {row['pickup_name']}, Pickup Address: {row['pickup_address']}, "
                    f"Generator Name: {row['generator_name']}, Generator Address: {row['generator_address']}"
        }
        for _, row in valid_routes.iterrows()
    ]

    layer = pdk.Layer(
        "ArcLayer",
        routes,
        get_source_position="from_coordinates",
        get_target_position="to_coordinates",
        get_width=5,
        get_tilt=15, 
        get_color=[255, 182, 193, 255],  
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=valid_routes['pickup_lat'].mean(),
        longitude=valid_routes['pickup_lng'].mean(),
        zoom=6
    )

    tooltip = {
        "html": "<b>Trans info:</b> {info}",
        "style": {
            "backgroundColor": "pink",
            "color": "white"
        }
    }

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style='mapbox://styles/mapbox/light-v10'
    ))
df = pd.read_csv(file_url)

if {'type_debris', 'waste_quantity', 'pickup_lat', 'pickup_lng', 'receiving_lat', 'receiving_lng', 'pickup_name', 'pickup_address', 'generator_name', 'generator_address'}.issubset(df.columns):
    draw_routes(df)
else:
    st.error('Columns not found')




