import pandas as pd
from fbprophet import Prophet
import numpy as np

def model_iteration(df, start_date='2021-01-20', end_date='2021-01-31'):

    start = df[df['ds'] == start_date].index[0]
    end = df[df['ds'] == end_date].index[0]

    predictions = {}
    for index in range(start, end):
        model = Prophet(interval_width=0.95, weekly_seasonality=True,
                        changepoint_prior_scale=2)
        model.add_regressor("score")
        model.add_regressor("BTC_score")
        model.add_regressor("twitter_score")
        model.add_regressor("reddit_score")
        model.fit(df[:index])
        horizon = 1
        model_future = model.make_future_dataframe(horizon)
        model_future["score"] = df["score"]
        model_future["BTC_score"] = df["BTC_score"]
        model_future["twitter_score"] = df["twitter_score"]
        model_future["reddit_score"] = df["reddit_score"]
        forecast = model.predict(model_future)
        predictions[forecast['ds'][index]] = forecast['yhat'][index]

    real_preds = {}
    for key, value in predictions.items():
        real_preds[key.strftime('%Y-%m-%d')] = [value]

    actuals = df[start:][['ds','y']]

    real_preds = pd.DataFrame(real_preds)
    real_preds = real_preds.T
    real_preds = real_preds.reset_index()
    real_preds.columns = ['ds', 'pred']
    real_preds.ds = pd.to_datetime(real_preds.ds)

    comparision = pd.merge(actuals, real_preds, on='ds', how='left')
    comparision['mae'] = abs(comparision['y'] - comparision['pred'])
    comparision['actual_change'] = comparision['y']-comparision.shift(1)['y']
    comparision['pred_change'] = comparision['pred']-comparision.shift(1)['y']
    comparision['actual_change'] = np.where(comparision['actual_change'] > 0, 1, 0)
    comparision['pred_change'] = np.where(comparision['pred_change'] > 0, 1, 0)
    comparision['correct_pred'] = np.where(comparision['pred_change'] == comparision['actual_change'], 1, 0)

    comparision['previous_price'] = comparision.shift(1)['y']
    comparision['previous_pred_change'] = comparision.shift(1)['pred_change']
    comparision['future_change'] = comparision.shift(-1)['pred_change']

    return comparision


def wallet(budget, df, start='2021-01-11', end='2021-01-31'):
    start = df[df['ds'] == start].index[0]
    end = df[df['ds'] == end].index[0]
    new_df = df[start:end]

    cash = budget
    btc_value = 0

    market_portfolio = (budget/new_df['y'][start])*new_df['y'][:end]
    portfolio_value = []
    transaction_dates = []
    for index, row in new_df.iterrows():

        if row['future_change']==1:
            if cash==0:
                transaction_dates.append(row['ds'])
                portfolio_value.append(btc_value*row['y'])

            else:
                btc_value = (cash/row['y'])

                transaction_dates.append(row['ds'])


                portfolio_value.append(cash)
                cash = 0


        if row['future_change']==0:
            if len(portfolio_value)==0:
                portfolio_value.append(budget)
                transaction_dates.append(row['ds'])
            else:
                transaction_dates.append(row['ds'])
                portfolio_value.append(portfolio_value[-1])
                if btc_value>0:
                    cash = btc_value*row['y']
                    btc_value = 0
    if cash == 0:
        return (portfolio_value[-1], portfolio_value, transaction_dates, market_portfolio)
    else:
        return (portfolio_value[-1], portfolio_value, transaction_dates, market_portfolio)
