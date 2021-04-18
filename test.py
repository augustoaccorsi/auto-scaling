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

#Figure Out Order for ARIMA Model
stepwise_fit = auto_arima(df['cpu'], suppress_warnings=True)           
print(stepwise_fit.summary())

#Split Data into Training and Testing
print(df.shape)
train=df.iloc[:-30]
test=df.iloc[-30:]
print(train.shape,test.shape)
print(test.iloc[0],test.iloc[-1])


#Train the Model
model=ARIMA(train['cpu'],order=(5,0,2))
model=model.fit()
print(model.summary())

#Make Predictions on Test Set
start=len(train)
end=len(train)+len(test)-1
#if the predicted values dont have date values as index, you will have to uncomment the following two commented lines to plot a graph
#index_future_dates=pd.date_range(start='2018-12-01',end='2018-12-30')
pred=model.predict(start=start,end=end,typ='levels').rename('ARIMA predictions')
#pred.index=index_future_dates
pred.plot(legend=True)
test['cpu'].plot(legend=True)
plt.show()

pred.plot(legend='ARIMA Predictions')
test['cpu'].plot(legend=True)
plt.show()

test['cpu'].mean()

rmse=sqrt(mean_squared_error(pred,test['cpu']))
print(rmse)

model2=ARIMA(df['cpu'],order=(5,0,2))
model2=model2.fit()
print(df.tail())


#For Future Dates
index_future_dates=pd.date_range(start='2018-12-30',end='2019-01-29')
#print(index_future_dates)
pred=model2.predict(start=len(df),end=len(df)+30,typ='levels').rename('ARIMA Predictions')
#print(comp_pred)
pred.index=index_future_dates
print(pred)

pred.plot(legend=True)
plt.show()