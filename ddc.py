import streamlit as st
import pandas as pd
import numpy as np

data=pd.read_csv('C:\Users\Lenovo\Desktop\LF_caps.cvs')
if st.checkbox('Show dataframe'):
  st.write(data)
