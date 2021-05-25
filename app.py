from flask import Flask, jsonify
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import numpy as np
from requests.sessions import session
from pickle import load
app=Flask(__name__)
@app.route('/')
def main():
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
        "Today's Rate":int(price_array),
        "Expected Price after 30 days":int(loaded_model.predict(price_array))
    }
    return jsonify(result)
if __name__=="__main__":
    app.run(debug=True)