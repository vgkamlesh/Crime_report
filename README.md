Crime Data Analysis and Prediction (India)

Overview
This project analyzes district-level crime data from 2016 to 2023 and predicts expected crime counts for 2024 using linear regression. The goal is to identify trends across different crime categories and estimate future values.

Features
Data cleaning and preprocessing from multiple Excel files
Standardization of district names
Merging of six crime categories IPC SLL Women Children SC ST
Combination of yearly data into a single dataset
Prediction of crime counts for 2024

Dataset Structure

Final dataset crime_data.csv contains
Year District IPC SLL Women Children SC ST

Prediction output crime_prediction_2024.csv contains
District Year Pred_IPC Pred_SLL Pred_Women Pred_Children Pred_SC Pred_ST

Methodology
For each district historical data from 2016 to 2023 is used to train a linear regression model. Year is used as the input feature and all six crime categories are predicted together using multi output regression.

Model
Linear Regression using scikit learn

Notes
Negative predictions are clipped to 0 since crime counts cannot be negative. Predictions are trend based estimates and not exact forecasts.

Project Structure
crime-project folder contains data folder src folder crime_data.csv crime_prediction_2024.csv README.md and requirements.txt

How to Run
Install dependencies using pip install -r requirements.txt
Run the script using python your_script.py

Dependencies
pandas numpy scikit-learn

Future Improvements
Add visualizations such as graphs or heatmaps
Create a district level safety score
Use more advanced time series models
Build a dashboard

Limitations
Only 7 to 8 data points per district due to lack of organised govt data
Linear model assumes simple trends
External factors are not considered

-By Kamlesh V G
