from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crypto_project.data import price_and_indexes
from crypto_project.model import fit_model,future_dataframe,model_predict



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def predict():

    # get data
    dataframe = price_and_indexes(local=False)
    # fit
    fitted_model = fit_model(dataframe,local=False)
    # make future dataframe
    model_future = future_dataframe(dataframe, fitted_model,local=False)
    # predict
    prediction = model_predict(fitted_model, model_future)
    #compare to the current bitcoin price
    current_btc_price = dataframe["y"][-1:].values[0]
    if prediction > current_btc_price:
        recommendation = "Buy"
    else:
        recommendation = "Sell"
    
    return {"prediction": prediction,
            "current_btc_price": current_btc_price,
            "Recommendation": recommendation
    }

    
