from binance.client import Client
import pandas as pd
from time import sleep
import config


client = Client(config.apiKey, config.apiSecurity)
print('logged in')

err = True
while err == True:
     try:
         df = pd.DataFrame(client.get_historical_klines('ADAUSDT', '15m', '10m UTC'))
         err = False
     except:
        print('something wrong')
        sleep(5)


print(df)
