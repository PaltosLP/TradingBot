from binance.client import Client
import pandas as pd
# import ta
# from time import sleep
# from termcolor import colored
import config






client = Client(config.apiKey, config.apiSecurity)
print('logged in')


def get_min_data(symbol, time_interval):
    utc_time = str(int(time_interval) * 60) + 'm UTC'
    interval = str(time_interval) + 'm'
    df = pd.DataFrame(client.get_historical_klines(symbol, interval, utc_time))
    df = df.iloc[:,:6]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df.set_index('Time')
    df.index = pd.to_datetime(df.index, unit='ms')
    df = df.astype(float)
    return df



data = get_min_data('ADAUSDT', 15)

print(data)


# f = open('demo_data.txt')
#
# f.write(data)
#
# f.close()
