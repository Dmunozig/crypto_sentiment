import numpy as np
import pandas as pd 
import requests

"""These function retrieve our API data and return dataframes"""

def price_and_indexes(local=True):
    
    if local==True:
        # Historic Bitcoin Prices
        btc_data = pd.read_csv('data/bitcoinprice_fixed.csv')
        btc_data.columns=['timestamp','btc_price']
        btc_data = btc_data.set_index('timestamp')

        # Fear & Greed index
        fear_greed_data = pd.read_csv('../data/Fear_Greed_df.csv')
        fear_greed_data = fear_greed_data.set_index('timestamp')

        # Augmento index
        augmento_data = pd.read_csv('../data/augmento_scores_df.csv')
        augmento_data = augmento_data.rename(columns={"datetime": "timestamp"})
        augmento_data = augmento_data.set_index('timestamp')

        complete_df = btc_data.join(fear_greed_data,on='timestamp',how='inner').join(augmento_data,on='timestamp',how='inner')

        return complete_df

        
    if local==False:
        # Historic Bitcoin Prices
        ## Due to size limit of API request, process needs to be split in two for out current time-frame
        return None
