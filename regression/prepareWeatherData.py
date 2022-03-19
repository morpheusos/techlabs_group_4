# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 10:50:37 2022

Use this file to clean up the historical weather data of Berlin that has been crawled from https://www.worldweatheronline.com/

@author: jtnjo
"""

import os
os.chdir("C:/Users/jtnjo/Documents/TL WS 2021 Projekt")

import pandas as pd
df = pd.read_excel("weather_data_berlin_2018_to_2020.xlsx")

# %% Generate datetime object from the columns
#Convert Time to string and remove the date info ("1900-00-00")
df["Time"] = df["Time"].astype("string") \
    .str.replace(pat = "^\d{4}-\d{2}-\d{2} ", repl = "", regex = True)

#Convert date to string
df["date_"] = df["date_"].astype("string")

#Concatenate Time and date and parse it as a datetime object
df["datetime"] = df["Time"] + " " + df["date_"]
df["datetime"] = pd.to_datetime(df["datetime"])

# %% Convert columns
#Remove Temp units and convert to numeric
df["Temp"] = df["Temp"].astype("string") \
    .str.replace(pat = ".{3}$", repl = "", regex = True)
df["Temp"] = pd.to_numeric(df["Temp"])

#Remove Rain units and convert to numeric
df["Rain"] = df["Rain"].astype("string") \
    .str.replace(pat = "mm", repl = "", regex = True)
df["Rain"] = pd.to_numeric(df["Rain"])

#Remove Cloud % sign and convert to numeric / 100
df["Cloud"] = df["Cloud"].astype("string") \
    .str.replace(pat = "%", repl = "", regex = True)
df["Cloud"] = pd.to_numeric(df["Cloud"]) / 100

#Remove Pressure units and convert to numeric
df["Pressure"] = df["Pressure"].astype("string") \
    .str.replace(pat = "mb", repl = "", regex = True)
df["Pressure"] = pd.to_numeric(df["Pressure"])

#Remove Wind units and convert to numeric
df["Wind"] = df["Wind"].astype("string") \
    .str.replace(pat = "\D", repl = "", regex = True)
df["Wind"] = pd.to_numeric(df["Wind"])

#Remove Gust  units and convert to numeric
df["Gust"] = df["Gust"].astype("string") \
    .str.replace(pat = "\D", repl = "", regex = True)
df["Gust"] = pd.to_numeric(df["Gust"])

# %% General cleanup
#Drop unused columns
df = df.drop(["Time", "Forecast", "Rain %", "Dir", "date_"], axis = 1)

#Rename columns 
df = df.rename(columns={
    "Temp": "temp_C", 
    "Rain": "rain_mm", 
    "Cloud": "cloud", 
    "Pressure": "pressure_mb", 
    "Wind": "wind_kmh", 
    "Gust" :"gust_kmh"})

# %%Add UTC timezone to timestamp
from datetime import timezone

df["datetime"] = df["datetime"].dt.tz_localize(timezone.utc)

# %% Export df to .csv file

df.to_csv("weather_data_berlin_2018_to_2020_clean.csv", index = False)