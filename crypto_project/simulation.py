import pandas as pd

def get_predictions(exog=False):

    if exog == True:
        predictions_df = pd.read_csv('../data/predictions_wscore_df')

        return predictions_df

    predictions_df = pd.read_csv('../data/predictions_df')
    return predictions_df

def wallet(budget, df, start='2019-06-19', end='2021-03-01'):
    start = df[df['ds']==start].index[0]
    end = df[df['ds']==end].index[0]
    new_df = df[start:end]

    cash = budget
    btc_value = 0

    portfolio_value = []
    transaction_dates = []
    for index, row in new_df.iterrows():

        if row['future_change']==1:
            if cash==0:
                pass

            else:
                btc_value = (cash/row['y'])

                transaction_dates.append(row['ds'])

                portfolio_value.append(cash)
                cash = 0


        if row['future_change']==0 and btc_value>0:
            cash = btc_value*row['y']
            btc_value = 0
            portfolio_value.append(cash)
            transaction_dates.append(row['ds'])

    if cash == 0:
        portfolio = btc_value*df[end:]['y'][end]
        return (portfolio, portfolio_value, transaction_dates)
    else:
        return (cash, portfolio_value, transaction_dates)

