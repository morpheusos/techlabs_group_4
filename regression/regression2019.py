# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 10:43:34 2022

@author: jtnjo
"""

import os
os.chdir("C:/Users/jtnjo/Documents/TL WS 2021 Projekt")

import numpy as np
import pandas as pd
import statsmodels.api as sm

# %% Read 2019 uber data and concatenate to single dataframe
files = ["./speeds/" + f for f in os.listdir("./speeds")]
working = pd.concat([pd.read_csv(f, parse_dates = ["utc_timestamp"]) for f in files ])
working= working.drop(["segment_id", "start_junction_id", "end_junction_id"], axis = 1)

working = working.sort_values(["utc_timestamp", "osm_start_node_id", "osm_end_node_id"])

# %% Join weather data and create dummies
weather = pd.read_csv("weather_data_berlin_2018_to_2020_clean.csv", parse_dates = ["datetime"])
working = pd.merge_ordered(working, weather, left_on = "utc_timestamp", right_on = "datetime", how = "left", fill_method = "ffill")

#hour dummies
hour_dummies = pd.get_dummies(data = working["hour"], prefix = "hour")
working = pd.concat([working, hour_dummies], axis = 1)

#weekday dummies
weekday_dummies = pd.get_dummies(data = (working["utc_timestamp"].dt.weekday + 1), prefix = "weekday")
working = pd.concat([working, weekday_dummies], axis = 1)

#month dummies
month_dummies = pd.get_dummies(data = working["month"], prefix = "month")
working = pd.concat([working, month_dummies], axis = 1)

#Drop NAs
working = working.dropna()


# %% Create DF with osm_way_id and number of observations with this id
osm_ids = pd.DataFrame(working["osm_way_id"].value_counts())
osm_ids = osm_ids.reset_index()
osm_ids = osm_ids.rename(mapper = {"index": "osm_way_id", "osm_way_id": "count"}, axis = 1)

#create list (all osm_ids with at least 100 rows)
target_ids = osm_ids[osm_ids["count"] >= 100]["osm_way_id"]

# %% Instantiate empty DataFrame to store the regression results per osm_way_id
columns_list = ["rsquared", "constant", "temp_C", "rain_mm", "cloud", "pressure_mb", "wind_kmh", 
                    'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6',
                    'hour_7', 'hour_8', 'hour_9', 'hour_10', 'hour_11', 'hour_12',
                    'hour_13', 'hour_14', 'hour_15', 'hour_16', 'hour_17', 'hour_18',
                    'hour_19', 'hour_20', 'hour_21', 'hour_22', 'hour_23', 
                    'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5','weekday_6', 'weekday_7',
                    'month_2', 'month_3', 'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9', 'month_10', 'month_11', 'month_12'
                    ]


regression_results = pd.DataFrame(columns = columns_list + ["osm_way_id"])

# %% Loop and execute regression for every id in target_ids
for i in target_ids:
    #Extract x and y values for the specified osm_way_id
    extracted_road = working.loc[working["osm_way_id"] == i, :]
    X = extracted_road[["temp_C", "rain_mm", "cloud", "pressure_mb", "wind_kmh", 
                        'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6',
                        'hour_7', 'hour_8', 'hour_9', 'hour_10', 'hour_11', 'hour_12',
                        'hour_13', 'hour_14', 'hour_15', 'hour_16', 'hour_17', 'hour_18',
                        'hour_19', 'hour_20', 'hour_21', 'hour_22', 'hour_23', 
                        'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5','weekday_6', 'weekday_7',
                        'month_2', 'month_3', 'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9', 'month_10', 'month_11', 'month_12'
                        ]].values;
    y = extracted_road["speed_kph_mean"].values;
    
    #Fit the model with statsmodels to give a summary of the model
    est = sm.OLS(y, sm.add_constant(X))
    est2 = est.fit()
    est2_robust = est2.get_robustcov_results(cov_type = "HC1")

    #Append the results to the regression_results DataFrame
    results = pd.DataFrame(data = np.append(est2_robust.rsquared, est2_robust.params).reshape(1,-1), columns = columns_list)
    results["osm_way_id"] = i
    results["n_observations"] = est2_robust.nobs

    regression_results = pd.concat([regression_results, results], axis = 0)
    
# %% Add osm street_names to regression_results
street_names = pd.read_csv("streetnamesOSM.csv")
regression_results = pd.merge(regression_results, street_names, left_on = "osm_way_id", right_on = "@id", how = "left")
regression_results = regression_results.drop(["@id"], axis = 1)

# %% Save regression_results to a csv
regression_results.to_csv("regression_results.csv", index = False)