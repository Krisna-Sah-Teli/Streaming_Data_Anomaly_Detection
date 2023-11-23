* PROJECT : ANOMALY DETECTION USING LOESS (STL)
This project done to explore the anomalies detection of time series data. Here parallely data is generated and its anomaly behavior is dectected.

- Detecting anomalies in a data stream with the ability to adapt to concept drift and seasonal variations is a challenging task. One algorithm that can address these challenges is the Seasonal-Trend decomposition using LOESS (STL) combined with an anomaly detection mechanism. STL is effective in decomposing time series data into seasonal, trend, and remainder components, making it suitable for handling seasonal variations. We can then use statistical methods to identify anomalies in the remainder component.
- PROCEDURE TO EXECUTE THE SYSTEM
-   First download whole repo
  - Install the required libraires. I have already created virtual env which contains all the neede libraries
  - Once everything is ready, just execute the following command
  - - python run.py
  - It will open a localhospot where you can see the anomaly detection chart. 
