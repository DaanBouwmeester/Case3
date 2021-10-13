import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
import json
import plotly.figure_factory as ff

st.write("Hello")

laadpaaldata = pd.read_csv('laadpaaldata.csv')
pd.set_option('display.max_columns', None)

#laadpaaldata.head() 
#laadpaaldata.info()
#laadpaaldata.describe()

#plt.hist(laadpaaldata['ConnectedTime'], bins = 50)
#plt.hist(laadpaaldata['TotalEnergy'], bins=50)
#plt.hist(laadpaaldata['ChargeTime'], bins=50)
#plt.hist(laadpaaldata['MaxPower'], bins=50)

laadpaaldata1 = laadpaaldata[laadpaaldata['ChargeTime'] >= 0 ]
#laadpaaldata1.describe()
