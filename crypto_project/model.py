from fbprophet import Prophet

def fit_model(dataframe):
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

def future_dataframe(fitted_model):

# define the horizon of the prediction
    horizon = 1
# create the future dataframe
    model_future = fitted_model.make_future_dataframe(horizon)
# create the regressors/features columns
    model_future["BTC_score"] = dataframe["BTC_score"] 
    model_future["twitter_score"] = dataframe["twitter_score"] 
    model_future["reddit_score"] = dataframe["reddit_score"] 
    model_future["Fear&Greed"] = dataframe["Fear&Greed"]
    return model_future
#predict
def model_predict(fitted_model, model_future):
    prediction = fitted_model.predict(model_future)
    return prediction


if __name__ == "__main__":
    # get data
    # df = get_data()
    # clean data
    # dataframe = clean_data(df)
    # fit
    fitted_model = fit_model(dataframe)
    # make future dataframe
    model_future = future_dataframe(fitted_model)
    # predict
    model_predict(fitted_model, model_future)
