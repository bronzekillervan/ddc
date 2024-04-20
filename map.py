import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim

# 初始化地理编码器
geolocator = Nominatim(user_agent="streamlit_app")

# 地理编码函数
def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        return (location.latitude, location.longitude)
    except:
        return (None, None)

st.title('地址地图显示应用')

# 文件上传器
uploaded_file = st.file_uploader("请选择表格文件", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # 根据文件类型读取数据
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 检查表中是否含有正确的列名
    if 'pickup_address' in df.columns and 'receiving_address' in df.columns:
        # 应用地理编码函数
        df['pickup_coords'] = df['pickup_address'].apply(geocode_address)
        df['receiving_coords'] = df['receiving_address'].apply(geocode_address)

        # 展示经纬度数据
        st.dataframe(df[['pickup_address', 'pickup_coords', 'receiving_address', 'receiving_coords']])

        # 在地图上展示经纬度
        for _, row in df.iterrows():
            if row['pickup_coords'] != (None, None) and row['receiving_coords'] != (None, None):
                st.map([row['pickup_coords'], row['receiving_coords']])
    else:
        st.error('表格中没有找到正确的列名。请确保您的表格中包含 "pickup_address" 和 "receiving_address" 列。')
else:
    st.info('请上传一个文件来开始。')

