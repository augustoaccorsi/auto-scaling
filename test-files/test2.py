# https://github.com/nachi-hebbar/ARIMA-Temperature_Forecasting/blob/master/Temperature_Forecast_ARIMA.ipynb
# https://www.youtube.com/watch?v=8FCDpFhd1zk&t=158s

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

# Ignore harmless warnings
import warnings
warnings.filterwarnings("ignore")

#Read Data
data_xls = pd.read_excel('data-set\\test.xlsx', 'Sheet1', dtype=str, index_col=None)
data_xls.to_csv('data-set\\csvfile.csv', encoding='utf-8', index=False) 
df=pd.read_csv('data-set\\csvfile.csv', index_col='date',parse_dates=True)

df=df.dropna()
print('Shape of data',df.shape)
print(df.head())
print()

#Plot Your Data
df['cpu'].plot(figsize=(12,5))
plt.show()

#Check For Stationarity
def adf_test(dataset):
   dftest = adfuller(dataset, autolag = 'AIC')
   print("1. ADF : ",dftest[0])
   if  dftest[1] < 0.05:
      print("2. P-Value : "+ str(dftest[1])+" OK")
   else:
      print("2. P-Value : ", dftest[1])
   print("3. Num Of Lags : ", dftest[2])
   print("4. Num Of Observations Used For ADF Regression and Critical Values Calculation :", dftest[3])
   print("5. Critical Values :")
   for key, val in dftest[4].items():
      print("\t",key, ": ", val)

adf_test(df['cpu'])
print()
