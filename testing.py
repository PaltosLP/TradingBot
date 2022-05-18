from binance.client import Client
import pandas as pd
import ta
from time import sleep
from termcolor import colored
import config


client = Client(config.apiKey, config.apiSecurity)
print('logged in')


def get_min_data(symbol, time_interval): 
        utc_time = str(int(time_interval) * 60) + 'm UTC'
        interval = str(time_interval) + 'm'
        time_err = True
        while time_err == True:
            try:
                df = pd.DataFrame(client.get_historical_klines(symbol, interval, utc_time))
                time_err = False
            except:
                print('something wrong with Timeout')
                sleep(10) 

        df = df.iloc[:,:6]
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df.set_index('Time')
        df.index = pd.to_datetime(df.index, unit='ms')
        df = df.astype(float)
        return df



df = get_min_data('ADAUSDT', 15)
print(ta.momentum.rsi(df.Close))

print('---------------------------------------------------------')

print(ta.momentum.rsi(df.Close).iloc[-1])

