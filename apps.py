# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 12:14:34 2023

@author: shrey
"""

import pandas as pd
import streamlit as st
from pickle import load
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing 

from PIL import Image
image = Image.open("apple_stock.jpeg")
st.image(image)


data_close = load(open('df3.pkl','rb'))

html_temp="""
<div style ="background-color:Black;padding:10px">
<h2 style="color:white;text-align:center;"> Forecasting Apple Stocks
"""

st.markdown(html_temp,unsafe_allow_html=True) 

periods = st.number_input('Enter the number of Days to forecast: ',min_value=1, max_value=365)

datetime = pd.date_range('2019-12-30', periods=periods)
s = pd.Series(pd.date_range('2019-12-30', periods=periods))
date_df = pd.DataFrame(s.dt.date,columns=['Date'])


df2 = pd.read_csv('AAPL.csv')
Train = df2.head(1760)
Test = df2.tail(251)

hwe_model_mul_add = ExponentialSmoothing(Train["Close"],seasonal="mul",trend="add",seasonal_periods=251).fit() 
pred_hwe_mul_add = hwe_model_mul_add.predict(start = Test.index[0],end = Test.index[-1])

hwe_model_mul_add = ExponentialSmoothing(df2.Close,seasonal="add",trend="add",seasonal_periods=251).fit()

y_pred = hwe_model_mul_add.predict(start=len(Train), end=len(Train)+len(Test)-1)

forecast = hwe_model_mul_add.forecast(steps=periods)

st.title('Forecasted values for specified period')
forecast_df = pd.DataFrame(forecast)
forecast_df.columns = ['Close']

# Forecasted values
data_forecast = forecast_df.set_index(date_df.Date)
st.write(data_forecast)

# low,medium,high
st.subheader('categorizing price in low,medium,high')
q1 = data_forecast['Close'].quantile(0.33)
q2 = data_forecast['Close'].quantile(0.66)

low = data_forecast['Close'][data_forecast['Close'] <= q1]
st.title('values in lower range')
low_df = pd.DataFrame(low)
low_df.columns = ['low']
low_df

medium = data_forecast['Close'][(data_forecast['Close'] > q1) & (data_forecast['Close'] <= q2)]
st.title('values in medium range')
medium_df = pd.DataFrame(medium)
medium_df.columns = ['medium']
medium_df

high = data_forecast['Close'][data_forecast['Close'] > q2]
st.title('values in higher range')
high_df = pd.DataFrame(high)
high_df.columns = ['high']
high_df

#Average
st.subheader('Average price of stocks for specified time frame')
avg = pd.Series(forecast)
st.write(avg.mean())

# Assuming data_forecast contains the forecasted values of Apple stock
st.title('Visualizing Forecasted values for specified period: ')
fig, ax = plt.subplots(figsize=(15, 15))
ax.plot(data_forecast, color='Green')
ax.set_title('Apple Stock Forecast',size=25)
ax.set_xlabel('Date', color='Blue',size=25)
ax.set_ylabel('Stock Price', color='Blue',size=25)
ax.grid(True)
# Add text labels for each data point
st.pyplot(fig)
plt.show()


