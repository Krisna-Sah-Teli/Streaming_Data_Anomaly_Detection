# app/routes.py

from flask import render_template, jsonify
from app import app
from datetime import datetime, timedelta
import pandas as pd
from statsmodels.tsa.seasonal import STL
from sklearn.ensemble import IsolationForest
import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN


def detect_anomalies(data_stream):
    seasonal_period= 180  # seasonal period of 6 months
    anomaly_threshold= 0.04

    # Apply Seasonal-Trend decomposition using LOESS (STL)
    stl = STL(data_stream, seasonal_period)
    result = stl.fit()
    seasonal, trend,  remainder= result.seasonal, result.trend, result.resid
    
    # Use Isolation Forest for anomaly detection
    isolation_forest = IsolationForest(contamination=anomaly_threshold)
    anomalies = isolation_forest.fit_predict(remainder.values.reshape(-1, 1))

    return anomalies


def generate_synthetic_data_stream(init= True):
    """
    Generate a synthetic data stream with regular patterns, seasonal elements, random noise,
    and occasional anomalies.

    Parameters:
    - num_points (int): Number of data points to generate.
    - period (int): Period of the regular pattern.
    - amplitude (float): Amplitude of the regular pattern.
    - noise_level (float): Standard deviation of the random noise.
    - anomaly_prob (float): Probability of introducing an anomaly at each time point.
    - anomaly_magnitude (float): Magnitude of the anomaly.

    Returns:
    - data_stream (numpy.ndarray): Array containing the generated synthetic data stream.
    """
    
    period=365   
    amplitude=10
    noise_level=0.75 
    anomaly_prob=0.05
    trend_convexity=0.01
    num_days=0
    start_date = datetime(2022, 1, 1)
    start_index=0

    if init==True:
        num_days= 365*2
        start_index=0
        # Load existing data
        try:
            df = pd.read_csv('app/static/synthetic_data.csv')
            df= df.iloc[0:0]   # Clearing the existing dataframe for newly initialized df
        except FileNotFoundError:
            df = pd.DataFrame(columns=['DateTime', 'Value'])
    else:
        num_days=30
        # Load existing data
        try:
            df = pd.read_csv('app/static/synthetic_data.csv')
            df= df.drop(range(30), axis=0)
            start_index= df.tail(1).index[0]+1
            start_date= pd.to_datetime(df.iloc[-1]["DateTime"]) 
            start_date= start_date+ timedelta(days=1) # to strart from next day          
        except FileNotFoundError:
            df = pd.DataFrame(columns=['DateTime', 'Value'])
            num_days=365*2+1  # As there is no any rows so first we add 2months data and extra one
    

    
    
    end_date = start_date + timedelta(days=num_days-1)
    
    date_range = pd.date_range(start=(start_date), end=end_date, freq='D').date

    for i in range(num_days):
        day= start_index+ i
        # Regular pattern with sine wave
        regular_pattern = amplitude * np.sin(4 * np.pi * day / period)

        # Trending pattern
        quadratic_trend = trend_convexity * (day / 10)**1.35
        
        # Seasonal element (e.g., sinusoidal variation with a different period)
        seasonal_element = 5 * np.sin(2 * np.pi * day / (period * 10))

        # Random noise
        noise = np.random.normal(0, noise_level)

        # Introduce anomaly with given probability
        if np.random.rand() < anomaly_prob:
            anomaly_magnitude= np.random.randint(10, 20)
            anomaly = anomaly_magnitude * np.random.normal(0, 0.3)
        else:
            anomaly = 0

        # Combine components to form the data point
        data_point = regular_pattern + quadratic_trend + seasonal_element + noise + anomaly

        # Add the new row using append
        new_row= {"DateTime": date_range[i], "Value": data_point}
        df.loc[day] = new_row


    # new_df= pd.DataFrame({"DateTime": date_range, "Value": data_stream})     
    # new_df["DateTime"]= pd.to_datetime(new_df['DateTime']).dt.date
    

    # #Append new data to existing data
    # df= pd.concat([df, new_df], ignore_index= True)

    df.to_csv('app/static/synthetic_data.csv', index=False)


@app.route('/')
def index():    
    #call function to generate data for first time
    generate_synthetic_data_stream(init=True)
    return render_template('index.html')



@app.route('/get_latest_data')
def get_latest_data():
    #call function to add 1 new datapoint to the existing df
    generate_synthetic_data_stream(init=False)
    # Loading df
    df = pd.read_csv('app/static/synthetic_data.csv')
    latest_data = df.tail(180)  # Get the latest 3 months' data
    # Apply anomaly detection on it
    anomaly= detect_anomalies(df["Value"])
    latest_data["Anomaly"]= anomaly[-180:] 
    print(len(latest_data))
 
    return jsonify(latest_data.to_dict(orient='records'))
