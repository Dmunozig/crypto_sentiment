import numpy as np
import pandas as pd 
import requests
from datetime import date

"""These function retrieve our API data and return dataframes"""

def price_and_indexes(local=True):
    
    if local==True:
        # Historic Bitcoin Prices
        btc_data = pd.read_csv('~/code/Dmunozig/crypto_project/data/bitcoinprice_fixed.csv') # Will these paths works if deployed?
        btc_data.columns=['timestamp','btc_price']
        btc_data = btc_data.set_index('timestamp')

        # Fear & Greed index
        fear_greed_data = pd.read_csv('~/code/Dmunozig/crypto_project/data/Fear_Greed_df.csv')
        fear_greed_data = fear_greed_data.set_index('timestamp')

        # Augmento index
        augmento_data = pd.read_csv('~/code/Dmunozig/crypto_project/data/augmento_scores_df.csv')
        augmento_data = augmento_data.rename(columns={"datetime": "timestamp"})
        augmento_data = augmento_data.set_index('timestamp')

        complete_df = btc_data.join(fear_greed_data,on='timestamp',how='inner').join(augmento_data,on='timestamp',how='inner')
        complete_df.fillna(value=complete_df['twitter_score'].mean(), inplace=True)

        return complete_df

        
    if local==False:
        date_today = str(date.today())

        # Historic Bitcoin Prices
        ## Due to size limit of API request, process needs to be split in two for out current time-frame
        first_url = "https://api.coindesk.com/v1/bpi/historical/close.json?start=2018-01-01&end=2020-09-26"
        first_batch = requests.get(first_url).json()
        second_url = "https://api.coindesk.com/v1/bpi/historical/close.json?start=2020-09-27&end=" + date_today
        second_batch = requests.get(second_url).json()

        first_df = pd.DataFrame.from_dict(first_batch["bpi"], orient='index')
        second_df = pd.DataFrame.from_dict(second_batch["bpi"], orient='index')
        btc_data = pd.concat([first_df, second_df], axis=0)
        btc_data.reset_index(level=0, inplace=True)
        btc_data.columns=['ds','y']
        btc_data['ds'] = pd.to_datetime(btc_data['ds'],format='%Y-%m-%d')
        btc_data = pd.DataFrame(btc_data)


        # Fear & Greed index
        url = 'https://api.alternative.me/fng/?limit=0'
        params = {'date_format' : 'world'}
        data = requests.get(url,params=params).json()
        fg_data = pd.DataFrame(data['data']).drop(columns=['value_classification','time_until_update'])
        fg_data['timestamp'] = pd.to_datetime(fg_data['timestamp'],format='%d-%m-%Y')
        fg_data.columns = ['Fear&Greed', 'ds']
        fg_data = pd.DataFrame(fg_data)

        complete_df = pd.merge(btc_data,fg_data, how='inner', left_on='ds', right_on='ds')

        return complete_df
