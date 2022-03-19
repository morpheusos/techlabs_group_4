"""
Created on Mon Mar  7 18:30:04 2022

@author: tim
"""
#%% imports
import streamlit as st 
import pandas as pd 
import numpy as np
import math
import pydeck as pdk

#%% website

#%%% window setup
st.set_page_config(
    page_title='Digital Shapers',
    page_icon=':computer:'    
    )

#%%% information
st.title('Group 4')
st.text(
        '''Members:     Georgios Emmanouilidis, Joshua Nguyen, Mahsa Khamanehasl, Tim Eulenberg
Mentor:     Fabian Schlüter''')
st.header('Traffic and weather analysis')
st.text(
"""
We used a uber dataset with information on movement speeds and scraped weather data to build a regression model that allowed us to analize to what degree a street is affected by the weather conditions.
The following dataframe represents our data, but so far i dont know the latitude and longitude of our nodes. Use the slider to see to which degree which coordinates are affected.
"""
)

#%%% the map
demo_frame = pd.DataFrame({
    'lat': [3.47659, 3.48679, 3.59603, 3.59867, 3.00222, 3.85622, 3.55720],
    'lon': [23.87260, 23.90500, 23.90532, 23.77616, 23.32388, 3.84777, 23.12211],
    'rsquared': [0.13, 0.15, 0.22, 0.0, 0.11, 0.31, 0.225] 
    })
demo_frame['rsquared_inverted_floor'] = demo_frame['rsquared'].apply(lambda x: math.floor((1-x)*10))
x = st.slider('affectedness by weather', max_value = 10)
st.map(demo_frame[demo_frame['rsquared_inverted_floor'] == x])

#%%% the frame
st.text('this is the sample frame you see on the widget above:')
demo_frame

#%%% the search "engine"
our_frame = pd.read_csv('regressions.csv')
street = st.text_input('Enter a streetname to see its data')
if (our_frame['name'].str.contains(street).sum()) > 0: 
    result = our_frame[our_frame['name'] == street]
    st.write(result)
elif street == '':
    #nothing entered no exception needed.
    nonsense = 0
else:
    st.error('there is no street with this name in the dataset, check for spelling or try a different street')
    
#%%% second attempt for a map
#CATTLE_DATA = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/nm_cattle.csv"
POULTRY_DATA = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/nm_chickens.csv"


HEADER = ["lng", "lat", "weight"]
#cattle_df = pd.read_csv(CATTLE_DATA, header=None).sample(frac=0.5)
poultry_df = pd.read_csv(POULTRY_DATA, header=None).sample(frac=0.5)

#cattle_df.columns = HEADER
poultry_df.columns = HEADER

COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]


view = pdk.data_utils.compute_view(cattle_df[["lng", "lat"]])
view.zoom = 6

"""
cattle = pdk.Layer(
    "HeatmapLayer",
    data=cattle_df,
    opacity=0.9,
    get_position=["lng", "lat"],
    aggregation=pdk.types.String("MEAN"),
    color_range=COLOR_BREWER_BLUE_SCALE,
    threshold=1,
    get_weight="weight",
    pickable=True,
)
"""

poultry = pdk.Layer(
    "HeatmapLayer",
    data=poultry_df,
    opacity=0.9,
    get_position=["lng", "lat"],
    threshold=0.75,
    aggregation=pdk.types.String("MEAN"),
    get_weight="weight",
    pickable=True,
)


r = pdk.Deck(
    layers=[poultry],
    initial_view_state=view,
    map_provider="mapbox",
    map_style=pdk.map_styles.SATELLITE,
    tooltip={"text": "Concentration of cattle in blue, concentration of poultry in orange"},
)

st.write(r)
