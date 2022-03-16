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
our_frame = pd.read_csv('C:/Users/x-tim/Downloads/website_frame.csv')
street = st.text_input('Enter a streetname to see its data')
if (our_frame['street_name'].str.contains(street).sum()) > 0: 
    result = our_frame[our_frame['street_name'] == street]
    st.write(result)
elif street == '':
    #nothing entered no exception needed.
    nonsense = 0
else:
    st.error('there is no street with this street_name in the dataset, check for spelling or try a different street')
    
#%%% second attempt for a map
# layer = pdk.Layer(
#     'HexagonLayer',  # `type` positional argument is here
#     our_frame,
#     get_position=['osm_start_node_id'],
#     auto_highlight=True,
#     elevation_scale=50,
#     pickable=True,
#     elevation_range=[0, 3000],
#     extruded=True,
#     coverage=1)

# # Set the viewport location
# view_state = pdk.ViewState(
#     longitude=-1.415,
#     latitude=52.2323,
#     zoom=6,
#     min_zoom=5,
#     max_zoom=15,
#     pitch=40.5,
#     bearing=-27.36)

# # Combined all of it and render a viewport
# r = pdk.Deck(layers=[layer], initial_view_state=view_state)
# st.write(r)

#####
df = our_frame
#  pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/streets-v11',
     initial_view_state=pdk.ViewState(
         latitude=37.76,
         longitude=-122.4,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='osm_start_node_id',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
     ],
 )
)