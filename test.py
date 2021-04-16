import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import warnings


data_xls = pd.read_excel('data-set\\test.xlsx', 'Sheet1', dtype=str, index_col=None)
data_xls.to_csv('data-set\\csvfile.csv', encoding='utf-8', index=False)

df=pd.read_csv('data-set\\csvfile.csv',index_col='Datetime',parse_dates=True)
#df=df.dropna()
print('Shape of data',df.shape)
#df.head()
#print(df.head())
df

#df.asfreq('min')


df['CPU Utilization'].plot(figsize=(12,5))

df["CPU Utilization"]
df = df.cumsum()
plt.show()

print()

from statsmodels.tsa.stattools import adfuller

def ad_test(dataset):
     dftest = adfuller(dataset, autolag = 'AIC')
     print("1. ADF : ",dftest[0])
     if  dftest[1] < 0.05:
        print("2. P-Value : "+ str(dftest[1])+" OK")
     else:
        print("2. P-Value : ", dftest[1])
     print("3. Num Of Lags : ", dftest[2])
     print("4. Num Of Observations Used For ADF Regression:",      dftest[3])
     print("5. Critical Values :")
     for key, val in dftest[4].items():
         print("\t",key, ": ", val)

print("CPU Utilization")
ad_test(df['CPU Utilization'])
print()

print("Network In")
ad_test(df['Network In'])
print()

print("Network Out")
ad_test(df['Network Out'])
print()


warnings.filterwarnings("ignore")

stepwise_fit_cpu = auto_arima(df['CPU Utilization'], trace=True, suppress_warnings=True)

print(df.shape)
train=df.iloc[:-30]
test=df.iloc[-30:]
print(train.shape,test.shape)


model=ARIMA(train['CPU Utilization'],order=(2,1,2))
model=model.fit()
model.summary()

start=len(train)
end=len(train)+len(test)-1
pred=model.predict(start=start,end=end,typ='levels').rename('ARIMA Predictions')
print(pred)
pred.plot(legend=True)

test.asfreq('min')

test['CPU Utilization'].plot(figsize=(12,5))

test["CPU Utilization"]
test = test.cumsum()
plt.show()


'''
test['CPU Utilization'].plot(legend=True)

plt.plot(test['CPU Utilization'])
plt.show()
'''

test['CPU Utilization'].mean()
print(test['CPU Utilization'].mean())
rmse=sqrt(mean_squared_error(pred,test['CPU Utilization']))
print("CPU Utilization Accuracy: "+str(rmse))


model2=ARIMA(df['CPU Utilization'],order=(2,1,2))
model2=model2.fit()
#print(df.tail())

pred=model2.predict(start=len(df), end=len(df)+30,typ='levels').rename('ARIMA Predictions')
print(pred)

'''
pred.index = pred.index.to_series().astype(str)

pred.plot(legend=True)
pred['CPU Utilization'].plot(legend=True)
plt.plot(pred['CPU Utilization'])
plt.show()
'''
'''
df["CPU Utilization"]
df = df.cumsum()
plt.show()
'''
