import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
from fbprophet import Prophet

daily_df = pd.read_excel('teste.xlsx')
daily_df.head(10)

daily_df.groupby('EC').sum().sort_values('TRN_TOTAL')
daily_df = daily_df[daily_df['EC'] == 'SUPER MERCADO NAZARE']


daily_df.groupby('CEP').sum().sort_values('TRN_TOTAL')
daily_df = daily_df[daily_df['CEP'] == '66023000']

daily_df = daily_df.groupby('DATA')['TRN_TOTAL'].sum()

daily_df = daily_df.resample('D').apply(sum)
plt.plot(daily_df)
plt.show()

weekly_df = daily_df.resample('W').apply(sum)
plt.plot(weekly_df)
plt.show()

#########################################################################
df = daily_df.reset_index()
df.columns = ['ds', 'y']
df.tail(n=3)

prediction_size = 15
train_df = df[:-prediction_size]
train_df.tail(n=3)

m = Prophet(yearly_seasonality=False,weekly_seasonality=False,
            daily_seasonality=False).add_seasonality(
            name='w',period=7,fourier_order=20).add_seasonality(
            name='m',period=30.5,fourier_order=20)
m.fit(train_df)

future = m.make_future_dataframe(periods=prediction_size)
future.tail(n=3)

forecast = m.predict(future)
forecast.tail(n=10)

m.plot(forecast)
m.plot_components(forecast)

a = forecast.set_index('ds')[['yhat']].join(df.set_index('ds'))
a['diff'] = a['y']-a['yhat']
######     % de erro      ########################################
1-(a['diff'].sum()/a['y'].sum())