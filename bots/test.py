from binance.client import Client
from binance.exceptions import BinanceAPIException # here
import pandas as pd 
import ta 
from time import sleep
from termcolor import colored
from datetime import datetime
import config


client = Client(config.apiKey, config.apiSecurity)
print('logged in')


class Bot:

    def __init__(self, symbol, time_interval, strategy, sleep_time):
        self.symbol = symbol 
        self.time_interval = time_interval
        self.strategy = strategy
        self.sleep_time = sleep_time
        self.buying_asset = symbol[0:3]
        self.stable_asset = symbol[3:len(symbol)+1]

    def acc_data(self, asset):
            balance = dict()
            balance = client.get_asset_balance(asset = asset)
            return balance["free"]



    def get_min_data(self): 
        utc_time = str(int(self.time_interval) * 60) + 'm UTC'
        interval = str(self.time_interval) + 'm'
        time_err = True
        client = Client(config.apiKey, config.apiSecurity)
        while time_err == True:
            try:
                df = pd.DataFrame(client.get_historical_klines(self.symbol, interval, utc_time))
                time_err = False
            except BinanceAPIException as e:
                print(e)
                print('something wrong with Timeout')
                sleep(300)
                client = None
                client = Client(config.apiKey, config.apiSecurity)
                sleep(self.sleep_time)
                continue



        df = df.iloc[:,:6]
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df.set_index('Time')
        df.index = pd.to_datetime(df.index, unit='ms')
        df = df.astype(float)
        return df


bot = Bot('ADAUSDT', 15, 'macd', 60 )

print(bot.get_min_data())



