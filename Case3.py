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
#plt.hist(laadpaaldata1['ChargeTime'], bins=50)

laadpaaldata1 = laadpaaldata1[laadpaaldata1['ConnectedTime']<=50]
laadpaaldata1 = laadpaaldata1[laadpaaldata1['ChargeTime']<=15]
laadpaaldata1['Percentage opladen'] = laadpaaldata1['ChargeTime'] / laadpaaldata1['ConnectedTime']
#laadpaaldata1.head()

#laadpaaldata1.info()
#plt.scatter(y=laadpaaldata1['TotalEnergy'], x=laadpaaldata1['ChargeTime'])

#laadpaaldata1['ConnectedTime'].median()
#laadpaaldata1['ChargeTime'].median()
#laadpaaldata1['ConnectedTime'].mean()
#laadpaaldata1['ChargeTime'].mean()

fig = go.Figure()
for col in ['ConnectedTime', 'ChargeTime']:
    fig.add_trace(go.Histogram(x=laadpaaldata1[col]))


dropdown_buttons = [
    {'label': 'Connected Time', 'method': 'update',
    'args': [{'visible': [True, False]},
            {'title': 'Connected Time'}]},
    {'label': 'Charge Time', 'method': 'update',
    'args': [{'visible': [False, True]},
            {'title': 'Charge Time'}]}]

float_annotation = {'xref': 'paper', 'yref': 'paper',
                    'x': 0.95, 'y': 0.95,'showarrow': False,
                    'text': 'Median Connected Time is 3.5 hours' + '<br>' + 'Mean Connected Time is 5.2 hours' + '<br>' + 'Median Charge Time is 2.2 hours' + '<br>' + 'Mean Charge Time is 2.3 hours',
                    'font' : {'size': 10,'color': 'black'}
                    }

fig.data[1].visible=False
fig.update_layout({'updatemenus':[{'type': "dropdown",'x': 1.3,'y': 0.5,'showactive': True,'active': 0,'buttons': dropdown_buttons}]})
fig.update_layout(xaxis_title='Time in hour',
                  yaxis_title="Number of observations")
fig.update_layout({'annotations': [float_annotation]})

st.plotly_chart(fig)

laadpaaldata1 = laadpaaldata1[laadpaaldata1['ConnectedTime']<=20]
laadpaaldata1 = laadpaaldata1[laadpaaldata1['ChargeTime']<=6]

group_1 = laadpaaldata1['ConnectedTime']
group_2 = laadpaaldata1['ChargeTime']

hist_data = [group_1, group_2]
group_labels = ['Connected Time', 'Charge Time']

fig = ff.create_distplot(hist_data, group_labels, colors=['blue','red'])
fig.update_layout({'title': {'text':'Distplot of Charge and Connecting Time'},
                   'xaxis': {'title': {'text':'Time in hours'}}})

st.plotly_chart(fig)



