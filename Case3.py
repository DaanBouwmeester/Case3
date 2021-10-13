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

#laadpaaldata1['ConnectedTime'].mean()
#laadpaaldata1['ChargeTime'].mean()
#laadpaaldata1['Percentage opladen'].mean()

fig = go.Figure()
for col in ['ConnectedTime', 'ChargeTime']:
    fig.add_trace(go.Scatter(x=laadpaaldata1[col], y=laadpaaldata1['TotalEnergy'], mode='markers'))

my_buttons = [{'label': 'Connected Time', 'method': 'update',
    'args': [{'visible': [True, False, False]},
            {'title': 'Connected Time'}]},
    {'label': 'Charge Time', 'method': 'update',
    'args': [{'visible': [False, True, False]},
            {'title': 'Charge Time'}]},
    {'label': 'Combined', 'method': 'update',
    'args': [{'visible': [True, True, True]},
            {'title': 'Combined'}]}]

fig.update_layout({
    'updatemenus': [{
      'type':'buttons','direction': 'down',
      'x': 1.3,'y': 0.5,
      'showactive': True, 'active': 0,
      'buttons': my_buttons}]})    
fig.update_layout(xaxis_title='Time in hour',
                  yaxis_title="Total energy used in Wh")
fig.data[1].visible=False

st.plotly_chart(fig)

url = 'https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=10000&key=74e5c90d-3e4f-4bbe-b506-233af06f55ca'
r = requests.get(url)
datatxt = r.text
datajson = json.loads(datatxt)

df = pd.json_normalize(datajson)
#df.head()

#df['AddressInfo.Country.Title'].unique()
#pd.set_option('max_columns', None)

labels = ['UserComments', 'PercentageSimilarity','MediaItems','IsRecentlyVerified','DateLastVerified',
         'UUID','ParentChargePointID','DataProviderID','DataProvidersReference','OperatorID',
         'OperatorsReference','UsageTypeID','GeneralComments','DatePlanned','DateLastConfirmed','MetadataValues',
         'SubmissionStatusTypeID','DataProvider.WebsiteURL','DataProvider.Comments','DataProvider.DataProviderStatusType.IsProviderEnabled',
         'DataProvider.DataProviderStatusType.ID','DataProvider.DataProviderStatusType.Title',
         'DataProvider.IsRestrictedEdit','DataProvider.IsOpenDataLicensed','DataProvider.IsApprovedImport',
         'DataProvider.License','DataProvider.DateLastImported','DataProvider.ID','DataProvider.Title',
         'OperatorInfo.Comments','OperatorInfo.PhonePrimaryContact','OperatorInfo.PhoneSecondaryContact',
         'OperatorInfo.IsPrivateIndividual','OperatorInfo.AddressInfo','OperatorInfo.BookingURL',
         'OperatorInfo.ContactEmail','OperatorInfo.FaultReportEmail','OperatorInfo.IsRestrictedEdit',
         'UsageType','OperatorInfo','AddressInfo.DistanceUnit','AddressInfo.Distance','AddressInfo.AccessComments',
         'AddressInfo.ContactEmail','AddressInfo.ContactTelephone2','AddressInfo.ContactTelephone1',
         'OperatorInfo.WebsiteURL','OperatorInfo.ID','UsageType.ID','StatusType.IsUserSelectable',
         'StatusType.ID','SubmissionStatus.IsLive','SubmissionStatus.ID','SubmissionStatus.Title',
         'AddressInfo.CountryID','AddressInfo.Country.ContinentCode','AddressInfo.Country.ID',
         'AddressInfo.Country.ISOCode','AddressInfo.RelatedURL','Connections']
df = df.drop(columns=labels)

#df.head(30)

#df['NumberOfPoints'].sum()
#df['OperatorInfo.Title'].unique()

#df['UsageCost'].unique()
mappings = {'free':'Free',  '':'Unknown', 'Paod':'Paid','unknown':'Unknown','free at the bicycle chargeplace':'Free',
           'Gratis':'Free', 'gratis':'Free'}
df['UsageCost1'] = df['UsageCost'].replace(mappings)

fig = go.Figure()
for col in ['OperatorInfo.Title', 'UsageCost1']:
    fig.add_trace(go.Histogram(x=df[col]))


dropdown_buttons = [
    {'label': 'Operator', 'method': 'update',
    'args': [{'visible': [True, False]},
            {'title': 'Operator of Charging Station'}]},
    {'label': 'Usage Cost', 'method': 'update',
    'args': [{'visible': [False, True]},
            {'title': 'Usage Cost of Charging Station'}]}]


fig.data[1].visible=False
fig.update_layout({'updatemenus':[{'type': "dropdown",'x': 1.3,'y': 0.5,'showactive': True,'active': 0,'buttons': dropdown_buttons}]})
fig.update_xaxes(tickangle = -45)
st.plotly_chart(fig)

df['LAT'] = df['AddressInfo.Latitude']
df['LNG'] = df['AddressInfo.Longitude']

m = folium.Map(location = [52.0893191, 5.1101691], 
               zoom_start = 7)

for row in df.iterrows():
    row_values = row[1]
    location = [row_values['LAT'], row_values['LNG']]
    marker = folium.Marker(location = location,
                         popup = row_values['AddressInfo.AddressLine1'])
    marker.add_to(m)

folium_static(m)

#HIER KOMT CODE VAN DATASET VAN RDW, HIERNA ZULLEN WE EEN NIEUW VERKLEIND CSV BESTAND INLADEN IVM MET DE DATA LIMIET.
#DE DATA DIE IS INGELADEN VAN RDW IS DUS SCHOONGEMAAKT EN DAARVAN EEN NIEUW CSV BESTAND GEMAAKT

#Elektrisch = pd.read_csv('Elektrische_voertuigen.csv')
#Elektrisch.head()
#Elektrisch.info()
#Elektrisch.describe()

#plt.hist(Elektrisch['Massa rijklaar'], bins = 40)
#plt.scatter(y=Elektrisch['Massa rijklaar'], x=Elektrisch['Massa ledig voertuig'])

#Elektrisch1 = Elektrisch[Elektrisch['Massa rijklaar'] > 750]
#Elektrisch1['Massa rijklaar'].hist(bins = 40)
#plt.show()

#pd.isna(Elektrisch1['Catalogusprijs']).sum()
#Elektrisch1['Catalogusprijs'].fillna(Elektrisch['Catalogusprijs'].mean(), inplace=True)
#data = ['Kenteken','Merk', 'Handelsbenaming', 'Inrichting', 'Eerste kleur', 'Massa rijklaar', 'Zuinigheidslabel', 'Catalogusprijs'] 
#df = Elektrisch1[data]

#pd.isna(df['Catalogusprijs']).sum()
#df['Zuinigheidslabel'].fillna(('Onbekend'), inplace=True)
#df['Zuinigheidslabel'].value_counts().sort_values()
#del df['Zuinigheidslabel']

#df['Catalogusprijs'].max()
#df1 = df[df['Catalogusprijs'] <= 200000]
#df1.info()

df1 = pd.read_csv('Elektrischdata')
#plt.hist(df1['Catalogusprijs'], bins=100)

#df1['Eerste kleur'].value_counts()
#df1['Inrichting'].value_counts()

#df1.groupby("Merk")['Handelsbenaming'].unique()
#df1["Merk"].unique()

mappings1 = {'TESLA MOTORS':'TESLA', 'BMW I': 'BMW', 'FORD-CNG-TECHNIK':'FORD', 'VW':'VOLKSWAGEN', 'VOLKSWAGEN/ZIMNY':'VOLKSWAGEN',
            'JAGUAR CARS': 'JAGUAR', 'ZIE BIJZONDERHEDEN':'Nan', 'VW-PORSCHE':'VOLKSWAGEN'}
df1["CarBrand"] = df1['Merk'].replace(mappings1)

fig = px.histogram(df1, x='CarBrand', 
                   title='Number of cars per brand',
                   labels={'CarBrand':'Brand of the car'}).update_xaxes(categoryorder='total descending')
st.plotly_chart(fig)

df12 = pd.read_csv('RDW')

fig = px.line(x=df12['Year'], y=df1['Kenteken'])
fig.update_layout(xaxis_title='Years',
                  yaxis_title="Number of Electric Vehicles",
                 title='Linechart of the number of vehicles per month')
st.plotly_chart(fig)


