import streamlit as st
import pandas as pd
# 引入用于地图显示的库，例如geopy或其他地理编码库
from geopy.geocoders import Nominatim

# 设置Geopy的Nominatim服务
geolocator = Nominatim(user_agent="geoapiExercises")

# 用于地理编码地址的函数
def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        return (location.latitude, location.longitude)
    except:
        return (None, None)

st.title('地址地图显示应用')

# 文件上传器，用户可以上传表格文件
uploaded_file = st.file_uploader("请选择表格文件", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # 根据文件类型读取表格数据
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 确保pickup和receive地址列存在
    if 'pickup_address' in df.columns and 'receive_address' in df.columns:
        # 应用地理编码函数到地址列
        df['pickup_coords'] = df['pickup_address'].apply(geocode_address)
        df['receive_coords'] = df['receive_address'].apply(geocode_address)

        # 显示结果
        st.dataframe(df[['pickup_address', 'pickup_coords', 'receive_address', 'receive_coords']])
        
        # 在地图上显示起点和终点（假设geocode_address函数返回了有效的经纬度）
        for index, row in df.iterrows():
            if row['pickup_coords'] and row['receive_coords']:
                st.map([row['pickup_coords'], row['receive_coords']])
    else:
        st.error('表格中没有找到正确的地址列。请确保您的表格中包含"pickup_address"和"receive_address"列。')
else:
    st.info('请上传一个文件来开始。')
