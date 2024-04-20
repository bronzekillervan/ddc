import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# 初始化地理编码器
geolocator = Nominatim(user_agent="streamlit_app")

# 使用Streamlit的缓存装饰器来缓存地理编码的结果
@st.cache(allow_output_mutation=True)
def geocode_address(address):
    # 使用RateLimiter来避免过快地发送请求
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    try:
        location = geocode(address)
        if location:
            return (location.latitude, location.longitude)
    except Exception as e:
        st.error(f"Geocoding error: {e}")
        return (None, None)

st.title('地址地图显示应用')

# 文件上传器
uploaded_file = st.file_uploader("请选择表格文件", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # 根据文件类型读取数据
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    # 检查表中是否含有正确的列名
    if 'pickup_address' in df.columns and 'receiving_address' in df.columns:
        # 应用地理编码函数
        df['pickup_coords'] = df['pickup_address'].apply(geocode_address)
        df['receiving_coords'] = df['receiving_address'].apply(geocode_address)

        # 展示经纬度数据
        st.dataframe(df[['pickup_address', 'pickup_coords', 'receiving_address', 'receiving_coords']])

        # 准备一个新的DataFrame来存储所有坐标，以便批量渲染地图
        map_data = pd.DataFrame(
            [coords for coords in df[['pickup_coords', 'receiving_coords']].values.flatten() if coords is not None],
            columns=['lat', 'lon']
        )
        # 在地图上批量展示经纬度
        st.map(map_data)
    else:
        st.error('表格中没有找到正确的列名。请确保您的表格中包含 "pickup_address" 和 "receiving_address" 列。')
else:
    st.info('请上传一个文件来开始。')


