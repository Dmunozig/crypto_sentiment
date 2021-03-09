# Crypto Sentiment
This project is trying to predict the bitcoin price using sentiment analysis as an additional feature because the price is mainly linked to emotion/sentiment.   

# Motivation
As bitcoin prices is extremelly volatile due to its high speculative nature. A big part of the trading is backed by emotions and not fundamentals and logic. This project tries to capitalize on this inherently strong sentiment investing that makes up a majority of the trading of bitcoin. 


# Data Source 
The data was acquired from 3 different API's:
- https://www.coindesk.com/coindesk-api
- https://alternative.me/crypto/fear-and-greed-index/
- http://api-dev.augmento.ai/v0.1/documentation#introduction

# Models
- Prophet & Sarimax
- comparison
- model performance
- features

# Backtesting
- explaing how we backtested our strategy and what are the signals to buy and sell
- results comparison between a strategy with only the price and with the sentiment features

# Deployment

GCP & Heroku

# Front-End Web Framework
Streamlit (link to the repository below)
    - link here


Please document the project the better you can.

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
