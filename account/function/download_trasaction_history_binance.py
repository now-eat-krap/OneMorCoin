from datetime import datetime, timedelta
import ccxt
import pandas as pd
import math
from operator import itemgetter
import time
import os, sys, pickle

def connect(api_key,secret):
    exchange = ccxt.binance(config={
        'apiKey': api_key,
        'secret': secret,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future'
        }
    })
    
    return exchange

def get_transaction(exchange):
    year = 24 * 60 * 60 * 1000 * 365
    now = exchange.milliseconds ()
    get_transaction_id = []
    get_transaction_url = []
    file_name = []
    for _ in range(5):
        id = exchange.fapiPrivateGetIncomeAsyn({'startTime':now - year * (_+1), 'endTime':now - year *  _})
        if id['downloadId'] != None:
            get_transaction_id.append(id)
            start_date = datetime.fromtimestamp((now - year * (_+1))/1000)
            end_date = datetime.fromtimestamp((now - year * _)/1000)
            file_name.append(start_date.strftime("%Y%m%d") + "_" + end_date.strftime("%Y%m%d"))
    time.sleep(300)
    #get_transaction_id= [{'avgCostTimestampOfLast30d': '119981', 'downloadId': '840587914396434432'},
    # {'avgCostTimestampOfLast30d': '111244', 'downloadId': '840588123922157568'},
    # {'avgCostTimestampOfLast30d': '119981', 'downloadId': '840588333717811200'},
    # {'avgCostTimestampOfLast30d': '145685', 'downloadId': '840588543642697728'},]

    for _ in range(len(get_transaction_id)):
        if get_transaction_id[_]['downloadId'] != None:
           get_transaction_url.append(exchange.fapiPrivateGetIncomeAsynId({'downloadId':get_transaction_id[_]['downloadId']}))

    return get_transaction_url,file_name

def download(url, file_name, path):
    for _ in range(len(url)):
        with open(path+file_name[_]+".zip", "wb") as file:
            response = get(url[_]['url'])
            file.write(response.content)

def unzip(path, file_name):
    for _ in range(len(file_name)):
        os.system("mkdir " + path +file_name[_])
        os.system("unzip "+path+file_name[_]+" -d "+path+file_name[_]+"/")


#def main():
#    print("start")
#    if crypto_currency == "binance":
#        path_ = "/root/mysite/media/"
#        if user not in os.listdir(path_):
#            os.system("mkdir "+ path_ + user)

#        if api_key not in os.listdir(path_ + user + "/"):
#            os.system("mkdir "+ path_ + user + "/" + api_key)
#        else:
#            return

#        path = path_ + user + "/" + api_key+ "/"
#        if len(os.listdir(path)) == 0:
#            urls, file_name = get_transaction()
#            download(urls, file_name, path)
#            unzip(path, file_name)
#    print("end")
#if __name__ == '__main__':
#    main()
