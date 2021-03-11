import numpy as np
import pandas as pd 
import requests
from datetime import date
import os

"""These function retrieve our API data and return dataframes"""

def price_and_indexes(local=True):
    if local==True:
        # create the path for the file
        data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..",'data')
        # Historic Bitcoin Prices
        btc_data = pd.read_csv(os.path.join(data_path,"bitcoinprice_fixed.csv"))
        btc_data.columns=['timestamp','btc_price']
        btc_data = btc_data.set_index('timestamp')

        # Fear & Greed index
        fear_greed_data = pd.read_csv(os.path.join(data_path,"Fear_Greed_df.csv"))
        fear_greed_data = fear_greed_data.set_index('timestamp')

        # Augmento index
        augmento_data = pd.read_csv(os.path.join(data_path,"augmento_scores_df.csv"))
        augmento_data = augmento_data.rename(columns={"datetime": "timestamp"})
        augmento_data = augmento_data.set_index('timestamp')

        complete_df = btc_data.join(fear_greed_data,on='timestamp',how='inner').join(augmento_data,on='timestamp',how='inner')
        complete_df.fillna(value=complete_df['twitter_score'].mean(), inplace=True)

        # we are going to set the index date as a column in order to train with prophet
        #complete_df["timestamp"] = complete_df.index
        complete_df.reset_index(level=0, inplace=True)
        complete_df = complete_df[["timestamp","btc_price","Fear&Greed","BTC_score","twitter_score","reddit_score"]]
        complete_df.columns = ["ds","y","Fear&Greed","BTC_score","twitter_score","reddit_score"]
        complete_df.drop_duplicates(inplace=True)
        complete_df.reset_index(inplace=True)
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

        # Merge both datasets
        complete_df = pd.merge(btc_data,fg_data, how='inner', left_on='ds', right_on='ds')

        return complete_df


# get all augmento topics and return a dictionary
def get_augmento_topics():
    topics_url = "http://api-dev.augmento.ai/v0.1/topics"
    topics_index = requests.get(topics_url).json()
    return topics_index

# get all augmento topics count per day
def get_augmento_topics_count():
    url_agg = "http://api-dev.augmento.ai/v0.1/events/aggregated"
    # topics count for bitcoin in bitcointalk
    params_BTC_1 = {
    "source" : "bitcointalk",
    "coin" : "bitcoin",
    "bin_size" : "24H",
    "count_ptr" : 1000,
    "start_ptr" : 0,
    "start_datetime" : "2018-02-01T00:00:00Z",
    "end_datetime" : "2020-04-30T00:00:00Z",
    }
    data_BTC_1 = requests.get(url_agg, params=params_BTC_1).json()
    topics_count_BTC_1 = pd.DataFrame(data_BTC_1).drop(columns=['t_epoch'])
    topics_count_BTC_1['datetime'] = pd.to_datetime(topics_count_BTC_1['datetime']).dt.date
    topics_count_BTC_1 = topics_count_BTC_1.set_index('datetime')

    params_BTC_2 = {
    "source" : "bitcointalk",
    "coin" : "bitcoin",
    "bin_size" : "24H",
    "count_ptr" : 500,
    "start_ptr" : 0,
    "start_datetime" : "2020-04-29T00:00:00Z",
    "end_datetime" : "2021-03-02T00:00:00Z",
    }
    data_BTC_2 = requests.get(url_agg, params=params_BTC_2).json()
    topics_count_BTC_2 = pd.DataFrame(data_BTC_2).drop(columns=['t_epoch'])
    topics_count_BTC_2['datetime'] = pd.to_datetime(topics_count_BTC_2['datetime']).dt.date
    topics_count_BTC_2 = topics_count_BTC_2.set_index('datetime')

    # topics count for bitcoin in twitter
    params_twitter_1 = {
    "source" : "twitter",
    "coin" : "bitcoin",
    "bin_size" : "24H",
    "count_ptr" : 1000,
    "start_ptr" : 0,
    "start_datetime" : "2018-02-01T00:00:00Z",
    "end_datetime" : "2020-04-30T00:00:00Z",
    }
    data_twitter_1 = requests.get(url_agg, params=params_twitter_1).json()
    topics_count_twitter_1 = pd.DataFrame(data_twitter_1).drop(columns=['t_epoch'])
    topics_count_twitter_1['datetime'] = pd.to_datetime(topics_count_twitter_1['datetime']).dt.date
    topics_count_twitter_1 = topics_count_twitter_1.set_index('datetime')

    params_twitter_2 = {
    "source" : "twitter",
    "coin" : "bitcoin",
    "bin_size" : "24H",
    "count_ptr" : 500,
    "start_ptr" : 0,
    "start_datetime" : "2020-04-29T00:00:00Z",
    "end_datetime" : "2021-03-02T00:00:00Z",
    }
    data_twitter_2 = requests.get(url_agg, params=params_twitter_2).json()
    topics_count_twitter_2 = pd.DataFrame(data_twitter_2).drop(columns=['t_epoch'])
    topics_count_twitter_2['datetime'] = pd.to_datetime(topics_count_twitter_2['datetime']).dt.date
    topics_count_twitter_2 = topics_count_twitter_2.set_index('datetime')

    # topics count for bitcoin in reddit

    params_reddit_1 = {
    "source" : "reddit",
    "coin" : "bitcoin",
    "bin_size" : "24H",
    "count_ptr" : 1000,
    "start_ptr" : 0,
    "start_datetime" : "2018-02-01T00:00:00Z",
    "end_datetime" : "2020-04-30T00:00:00Z",
    }
    data_reddit_1 = requests.get(url_agg, params=params_reddit_1).json()
    topics_count_reddit_1 = pd.DataFrame(data_reddit_1).drop(columns=['t_epoch'])
    topics_count_reddit_1['datetime'] = pd.to_datetime(topics_count_reddit_1['datetime']).dt.date
    topics_count_reddit_1 = topics_count_reddit_1.set_index('datetime')

    params_reddit_2 = {
    "source" : "reddit",
    "coin" : "bitcoin",
    "bin_size" : "24H",
    "count_ptr" : 500,
    "start_ptr" : 0,
    "start_datetime" : "2020-04-29T00:00:00Z",
    "end_datetime" : "2021-03-02T00:00:00Z",
    }
    data_reddit_2 = requests.get(url_agg, params=params_reddit_2).json()
    topics_count_reddit_2 = pd.DataFrame(data_reddit_2).drop(columns=['t_epoch'])
    topics_count_reddit_2['datetime'] = pd.to_datetime(topics_count_reddit_2['datetime']).dt.date
    topics_count_reddit_2 = topics_count_reddit_2.set_index('datetime')

    # concatting dataframes
    topics_count_BTC_df = pd.concat([topics_count_BTC_1,topics_count_BTC_2])
    topics_count_twitter_df = pd.concat([topics_count_twitter_1,topics_count_twitter_2])
    topics_count_reddit_df = pd.concat([topics_count_reddit_1,topics_count_reddit_2])

    # rename columns
    topics_count_BTC_df.columns=['BTC_counts']
    topics_count_twitter_df.columns=['twitter_counts']
    topics_count_reddit_df.columns=['reddit_counts']

    # merge all dataframes
    topics_count_df = pd.merge(topics_count_BTC_df,topics_count_twitter_df,right_index=True,left_index=True).merge(topics_count_reddit_df,right_index=True,left_index=True)
    
    # classifying topics as neutral, positive and negative
    topics_index_value = {'0': 0,'1': -1,'2': 0, '3': -1,'4': 0,'5': 0,'6': -1,'7': 0,'8': 0,'9': 0,'10': 0,'11': 0,'12': 0,'13': 0,'14': -1,'15': 0,'16': -1,'17': 0,'18': 0,'19': 0,'20': 0,'21': 0,'22': 0,'23': 1,'24': 1,'25': 0,'26': -1,'27': -1,'28': 0,'29': 0,'30': 0,'31': 0,'32': -1,'33': 1,'34': 0,'35': 0,'36': 1,'37': -1,'38': 1,'39': 1,'40': -1,'41': 0,'42': 1,'43': 0,'44': 0,'45': 0,'46': 1,'47': 0,'48': -1,'49': 0,'50': 0,'51': 0,'52': 0,'53': -1,'54': -1,'55': 0,'56': 0,'57': 0,'58': 0,'59': 0,'60': 0,'61': 0,'62': 0,'63': 1,'64': -1,'65': 0,'66': 0,'67': 0,'68': 0,'69': 0,'70': 0,'71': 1,'72': 0,'73': -1,'74': 0,'75': 1,'76': 0,'77': 0,'78': 0,'79': 0,'80': 0,'81': -1,'82': 1,'83': 1,'84': -1,'85': -1,'86': 0,'87': 0,'88': 0,'89': -1,'90': 0,'91': 1,'92': -1}
    # function to create the scores
    def feature_creation(counts):
        positive_counts = []
        neg_counts = []
        for key, value in topics_index_value.items():
            if value==1:
                positive_counts.append(counts[int(key)])
            elif value==-1:
                neg_counts.append(counts[int(key)])
        
        X = (sum(positive_counts)+sum(neg_counts))
        
        if X==0:
            return np.NaN
        else:
            return sum(positive_counts)/X
    # apply the feature creation function on the dataframe to create new columns
    topics_count_df['BTC_score'] = topics_count_df['BTC_counts'].apply(feature_creation)
    topics_count_df['twitter_score'] = topics_count_df['twitter_counts'].apply(feature_creation)
    topics_count_df['reddit_score'] = topics_count_df['reddit_counts'].apply(feature_creation)
    # return only the columns with the scores
    scores_df = topics_count_df[['BTC_score','twitter_score','reddit_score']]
    return scores_df