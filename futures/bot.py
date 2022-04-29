import pandas as pd
from time import sleep
from binance.client import Client
import f_config


client = Client(f_config.apiKey, f_config.apiSecurity)
print('logged')
# balance = client.get_asset_balance(asset = 'USDT')
# print(balance)

# order = client.futures_create_order(symbol="ADAUSDT", side="BUY", type="MARKET", quantity=20)
# print(order)

info = client.futures_historical_klines('ADAUSDT', '15m', '10m UTC')
# print(info)

df = pd.DataFrame(client.get_historical_klines('ADAUSDT', '15m', '3600m UTC'))
df = df.iloc[:,:6]
df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
df = df.set_index('Time')
df.index = pd.to_datetime(df.index, unit='ms')
df = df.astype(float)
print(df)
