# Project Name: Crypto Sentiment
# Objective
This project predicts bitcoin prices using sentiment analysis as an additional feature because the price is mainly linked to emotion/sentiment.   

# Motivation
Bitcoin prices are extremely volatile due to its high speculative nature. A big part of the trading is backed by emotions and not fundamentals and logic. This project tries to capitalize on this inherently strong sentiment investing that makes up a majority of the trading of bitcoin. 

# Team
- Diego Munoz
    - https://github.com/Dmunozig
- Olavo W.S. Figueiredo
    - https://github.com/olavowsf
- Yassine Rkaibi
    - https://github.com/rkaibi
- Imamul Alam Majumder
    - https://github.com/theimo92

# Data Source 
The data was acquired from 3 different API's:
- https://www.coindesk.com/coindesk-api
- https://alternative.me/crypto/fear-and-greed-index/
- http://api-dev.augmento.ai/v0.1/documentation#introduction

# Model
- Prophet
# Other model tested:
- Sarimax
# Deployment
- GCP & Heroku

# Front-End Web Framework
Streamlit & link to the repository:
- https://cryptonite-sentiment.herokuapp.com/
- https://github.com/Dmunozig/Kryptonite-app

# Project Description

## Data
1. Identify datasets to use as exogenous features for the Prophet model.
2. Retrieve the data from chosen API's
3. Clean and explore the data.

## Modelling
1. Choose the period to train and test the model.
2. Tuning the model.

## Predicting
1. Make prediction for the next day.


## Backtesting
1. Create the buy and sell signal for the strategy.
2. Implement it across different time periods.
3. Compare strategy using only price with and without sentiment scores.

## Data Engineering
1. Package all the code into python files in order to deploy it.
2. Use Docker containers to deploy the back-end(prediciton API) on GCP.
3. Create the front-end with Streamlit and deploy it on Heroku.



# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for crypto_project in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/crypto_project`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "crypto_project"
git remote add origin git@github.com:{group}/crypto_project.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
crypto_project-run
```

# Install

Go to `https://github.com/{group}/crypto_project` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/crypto_project.git
cd crypto_project
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
crypto_project-run
```
