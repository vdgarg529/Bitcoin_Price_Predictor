from flask import Flask, jsonify
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import math
import pandas_datareader as web
import numpy as np
from requests.sessions import session
from pickle import load
#import tensorflow
#from tensorflow.keras.models import load_model
import datetime
today = datetime.date.today()
span30 = datetime.timedelta(days=30)
span2 = datetime.timedelta(days=2)
span1 = datetime.timedelta(days=1)
Next_30_date=today+span30
Prev_2_date=today-span2
Prev_1_date=today-span1
next_date=today+span1

app=Flask(__name__)

@app.route('/', methods=["GET"])
def main():
    result={
        "Bitcoin":"/CRYPTO/BITCOIN",
        "NIFT 50 Stocks":"/STOCKS/NIFTY50",
        "NIFT BANK Stocks":"/STOCKS/NIFTYBANK",
        "NIFT IT Stocks":"/STOCKS/NIFTYIT"
    }
    return jsonify(result)

@app.route('/CRYPTO/BITCOIN')
def bitcoin():
    url='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters={
        'start':'1',
        'limit':'1',
        'convert':'USD',

    }
    headers={
        'Acecpts': 'application/json',
        'X-CMC_PRO_API_KEY':'944f669d-87f0-4a45-a700-4e04d3b820b6',
    }
    session= Session()
    session.headers.update(headers)
    try:
        response=session.get(url,params=parameters)
        data=json.loads(response.text)
        price=data['data'][0]['quote']['USD']['price']
        price_array=np.array([[price]])
        #print(price_array)
    except(ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    loaded_model=load(open("bitcoin_predictor.pkl","rb"))
    result={
        "Type":"Bit-Coin",
        str(today):int(price_array),
        str(Next_30_date):int(loaded_model.predict(price_array))
    }
    return jsonify(result)
     
if __name__=="__main__":
    app.run()
