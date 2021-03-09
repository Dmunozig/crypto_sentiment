from fbprophet import Prophet
from crypto_project.data import price_and_indexes


# split the dataset into train and test dataframes
def train_test_split(dataframe):
    train  = dataframe.iloc[:-1]
    test = dataframe.iloc[-1:]
    return train, test

def fit_model(dataframe,local=True):
    if local==True:
        # instatiate the model   
        model = Prophet(interval_width=0.95, 
                                weekly_seasonality=True, 
                                changepoint_prior_scale=2)
        # add regressors
        model.add_regressor('BTC_score')
        model.add_regressor('twitter_score')
        model.add_regressor('reddit_score')
        model.add_regressor("Fear&Greed")
        # fit the model
        fitted_model = model.fit(dataframe)
        return fitted_model

    if local==False:
        # instatiate the model   
        model = Prophet(interval_width=0.95, 
                                weekly_seasonality=True, 
                                changepoint_prior_scale=2)
        # add regressor
        model.add_regressor("Fear&Greed")
        # fit the model
        fitted_model = model.fit(dataframe)
        return fitted_model



def future_dataframe(dataframe,fitted_model, local=True):
    if local==True:
        # define the horizon of the prediction
        horizon = 1
        # create the future dataframe
        model_future = fitted_model.make_future_dataframe(horizon)
        # create the regressors/features columns
        model_future["BTC_score"] = dataframe["BTC_score"] 
        model_future["twitter_score"] = dataframe["twitter_score"] 
        model_future["reddit_score"] = dataframe["reddit_score"] 
        model_future["Fear&Greed"] = dataframe["Fear&Greed"]
        # filling the future sentiment score with the previous day in order to be able to predict. Prophet is not able to predict with NaN values 
        model_future = model_future.fillna(method="ffill")
        return model_future

    if local==False:
        # define the horizon of the prediction
        horizon = 1
        # create the future dataframe
        model_future = fitted_model.make_future_dataframe(horizon)
        # create the regressors/features columns
        model_future["Fear&Greed"] = dataframe["Fear&Greed"]
        # filling the future sentiment score with the previous day in order to be able to predict. Prophet is not able to predict with NaN values 
        model_future = model_future.fillna(method="ffill")
        return model_future

#predict
def model_predict(fitted_model, model_future):

    prediction_dataframe = fitted_model.predict(model_future)
    prediction = prediction_dataframe["yhat"][-1:].values[0]
    return prediction


if __name__ == "__main__":
    # get data
    dataframe = price_and_indexes()
    # fit
    fitted_model = fit_model(dataframe)
    # make future dataframe
    model_future = future_dataframe(dataframe,fitted_model)
    # predict
    model_predict(fitted_model, model_future)
