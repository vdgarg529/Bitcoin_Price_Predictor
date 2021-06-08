from flask import Flask, jsonify
from flask_ngrok import run_with_ngrok
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import math
import pandas_datareader as web
import numpy as np
from requests.sessions import session
from pickle import load
from keras.models import load_model
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
run_with_ngrok(app)
TCS_model=load_model("TCS_model.h5")
TCS_scaler=load(open("TCS_scaler.pkl","rb"))
NIFTY50_model=load_model("NIFTY50_model.h5")
NIFTY50_scaler=load(open("NIFTY50_scaler.pkl","rb"))
NIFTYBANK_model=load_model("NIFTYBANK_model.h5")
NIFTYBANK_scaler=load(open("NIFTYBANK_scaler.pkl","rb"))
NIFTYIT_model=load_model("NIFTYIT_model.h5")
NIFTYIT_scaler=load(open("NIFTYIT_scaler.pkl","rb"))
TECHMAHINDRA_model=load_model("TECHMAHINDRA_model.h5")
TECHMAHINDRA_scaler=load(open("TECHMAHINDRA_scaler.pkl","rb"))
BHARTIAIRTEL_model=load_model("BHARTIAIRTEL_model.h5")
BHARTIAIRTEL_scaler=load(open("BHARTIAIRTEL_scaler.pkl","rb"))
TATAMOTORS_model=load_model("TATAMOTORS_model.h5")
TATAMOTORS_scaler=load(open("TATAMOTORS_scaler.pkl","rb"))
def predict(name): 
  quote=web.DataReader(name,data_source='yahoo',start='2012-01-01', end=str(Prev_1_date))
  new_df=quote.filter(['Close'])
  last_60_days=new_df.iloc[-60:].values
  last_60_days_scaled=scaler.transform(last_60_days)
  X_test=[]
  X_test.append(last_60_days_scaled)
  X_test=np.array(X_test)
  X_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
  pred_price=model.predict(X_test)
  pred_price=scaler.inverse_transform(pred_price)
  return (pred_price)
def last15dates():
  l=[]
  for i in range(15):
    span= datetime.timedelta(days=i)
    Prevdate=today-span
    l.append(Prevdate)
  return l

@app.route('/', methods=["GET"])
def main():
    result={
        "Bitcoin":"/CRYPTO/BITCOIN",
        "NIFT 50 Stocks":"/STOCKS/NIFTY50",
        "NIFT BANK Stocks":"/STOCKS/NIFTYBANK",
        "NIFT IT Stocks":"/STOCKS/NIFTYIT",
        "NIFT TCS Stocks":"/STOCKS/TCS",
        "NIFT TATA MOTORS Stocks":"/STOCKS/TATAMOTORS",
        "NIFT TECH MAHINDRA Stocks":"/STOCKS/TECHMAHINDRA",
        "NIFT BHARTI AIRTEL Stocks":"/STOCKS/BHARTIAIRTEL",
        
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
    #print(loaded_model.predict(price_array))
    result={
        "Type":"Bit-Coin",
        str(today):int(price_array),
        str(Next_30_date):int(loaded_model.predict(price_array))
    }
    return jsonify(result)
@app.route('/STOCKS/TCS')
def TCS():
    model=TCS_model
    
    test=test_data('TCS.NS')
    next=predict('TCS.NS')
    dte=last15dates()
    
    result={
        "Type":"Stock-TCS",
        str(next_date):int(next)
    }
    return jsonify(result)
@app.route('/STOCKS/NIFTY50')
def NIFTY50():
    model=NIFTY50_model
    
    test=test_data('^NSEI')
    next=predict('^NSEI')
    dte=last15dates()
    
    result={
        "Type":"Stock-NIFTY-50",
        str(next_date):int(next)
    }
    return jsonify(result)
@app.route('/STOCKS/NIFTYBANK')
def NIFTYBANK():
    model=NIFTYBANK_model
    
    test=test_data('^NSEBANK')
    next=predict('^NSEBANK')
    dte=last15dates()
    
    result={
        "Type":"Stock-NIFTY-BANK",
        str(next_date):int(next)
    }
    return jsonify(result)
@app.route('/STOCKS/NIFTYIT')
def NIFTYIT():
    model=NIFTYIT_model
    
    test=test_data('^CNXIT')
    next=predict('^CNXIT')
    dte=last15dates()
    
    result={
        "Type":"Stock-NIFTY-IT",
        str(next_date):int(next)
    }
    return jsonify(result)
@app.route('/STOCKS/TECHMAHINDRA')
def TECHMAHINDRA():
    model=TECHMAHINDRA_model
    
    test=test_data('TECHM.NS')
    next=predict('TECHM.NS')
    dte=last15dates()
    
    result={
        "Type":"Stock-TECH-MAHINDRA-LIMITED",
        str(next_date):int(next)
    }
    return jsonify(result)
@app.route('/STOCKS/BHARTIAIRTEL')
def BHARTIAIRTEL():
    model=BHARTIAIRTEL_model
    
    test=test_data('BHARTIARTL.NS')
    next=predict('BHARTIARTL.NS')
    dte=last15dates()
    
    result={
        "Type":"Stock-BHARTI-AIRTEL",
        str(next_date):int(next)
    }
    return jsonify(result)
@app.route('/STOCKS/TATAMOTORS')
def TATAMOTORS():
    model=TATAMOTORS_model
    
    test=test_data('TATAMOTORS.NS')
    next=predict('TATAMOTORS.NS')
    dte=last15dates()
    
    result={
        "Type":"Stock-TATA-MOTORS",
        str(next_date):int(next)
    }
    return jsonify(result)



     

if __name__=="__main__":
    app.run()
