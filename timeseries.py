import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import warnings
from statsmodels.tsa.stattools import adfuller


class Timeseries():

    def __init__(self, dataset_path, csv_path):
        self._data_xls = pd.read_excel(dataset_path, 'Sheet1', dtype=str, index_col=None)
        self._data_xls.to_csv(csv_path, encoding='utf-8', index=False)

        self._df=pd.read_csv('data-set\\csvfile.csv',index_col='Datetime',parse_dates=True)

        self._train = None
        self._test = None
        self._pred = None
        self._model = None
        self._rmse = None
        self._start = None
        self._end = None

        print('Shape of data',self._df.shape)
#self._df=self._df.dropna()
    def print_head(self):
        print(self._df.head())

    def plot_graph(self, dataset):
        self._df.asfreq('min')

        self._df[dataset].plot(figsize=(12,5))
        self._df[dataset]
        self._df = self._df.cumsum()

        plt.ylabel(dataset)
        plt.xlabel("Datetime (minutes)")

        plt.show()

    def stationary_test(self, dataset):
        print(dataset)
        dftest = adfuller(self._df[dataset], autolag = 'AIC')
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
    
    def auto_arima(self, dataset):
        return auto_arima(self._df[dataset], trace=True, suppress_warnings=True)

    def split_data(self):
        print(self._df.shape)
        self._train=self._df.iloc[:-30]
        self._test=self._df.iloc[-30:]
        print(self._train.shape,self._test.shape)

    def arima_model(self, dataset, order):
        #warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARMA', FutureWarning)
        #warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARIMA', FutureWarning)
        self._model=ARIMA(self._train[dataset],order=order)
        self._model=self._model.fit()
        self._model.summary()

    def check_model(self, dataset):
        self._start=len(self._train)
        self._end=len(self._train)+len(self._test)-1
        self._pred=self._model.predict(start=self._start,end=self._end,typ='levels').rename('ARIMA Predictions')
        print(self._pred)
        self._pred.plot(legend=True)
        #self._test[dataset].plot(legend=True)

        self._test.asfreq('min')

        self._test[dataset].plot(figsize=(12,5))

        self._test[dataset]
        self._test = self._test.cumsum()
        #plt.show()

    def check_accuracy(self, dataset):
        self._test[dataset].mean()
        self._rmse=sqrt(mean_squared_error(self._pred,self._test[dataset]))
        return self._rmse

if __name__ == '__main__':

    dataset = 'CPU Utilization'

    timeseries = Timeseries('data-set\\test.xlsx', 'data-set\\csvfile.csv')
    timeseries.print_head()
    #timeseries.plot_graph(dataset)
    timeseries.stationary_test(dataset)
    model = timeseries.auto_arima(dataset)
    #ARIMA(2,0,2)(0,0,0)[0] intercept
    order = model.get_params()['order']
    timeseries.split_data()
    timeseries.arima_model(dataset, order)
    timeseries.check_model(dataset)
    rmse = timeseries.check_accuracy(dataset)
    print(rmse)