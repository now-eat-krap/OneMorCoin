import pprint
from datetime import datetime, timedelta
import ccxt
import pandas as pd
import math
from operator import itemgetter
import time
import os, sys, pickle
import argparse, sys
from requests import get
from sqlalchemy import create_engine, text
import sqlalchemy
import pymysql

parser = argparse.ArgumentParser()
parser.add_argument('-user', help=' : Please set user (email address)') 
parser.add_argument('-crypto_currency', help=' : Please set crypto currency') 
parser.add_argument('-api_name', help=' : Please set api name') 
parser.add_argument('-api_key', help=' : Please set api key')
parser.add_argument('-api_secret', help=' : Please set api secret')
parser.add_argument('-crypto_id', help=' : Please set crypto id')

args = parser.parse_args()

user = args.user
crypto_currency = args.crypto_currency
api_name = args.api_name
api_key = args.api_key
secret = args.api_secret
crypto_id = args.crypto_id


exchange = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

def get_transaction():
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
    time.sleep(900)
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


def csv_to_dataframe(path):
    folder = os.listdir(path)
    folder_name = []
    for _ in range(len(folder)):
        if (folder[_])[-3:] != "zip":
            folder_name.append(folder[_])
    
    folder_name.sort()
    
    df = pd.DataFrame()
  
    for folder in folder_name:
        csv_path = os.listdir(path+folder)
        df1 = pd.read_csv(path+folder+"/"+csv_path[0])
        df = pd.concat([df,df1])

    # UTC to KST
    df['Date(UTC)'] = df['Date(UTC)'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d %H:%M:%S'))

    # datetime to timestamp
    df['timestamp'] = (df['Date(UTC)'].values.astype('int')/10**6).astype('int')

    df['Date(UTC)'] = df['Date(UTC)'] + timedelta(hours=9)
    df.rename(columns={'Date(UTC)':'Date'},inplace=True)

    # Amount object -> float
    df['Amount'] = df['Amount'].astype({'Amount':'float'})

    # funding_fee, transfer, insurance_clear
    funding_fees = df[df['type'] == 'FUNDING_FEE']
    transfers = df[df['type'] == 'TRANSFER']
    insurance_clears = df[df['type'] == 'INSURANCE_CLEAR']

    return df, funding_fees, transfers, insurance_clears

#get_download_id = exchange.fapiPrivateGetIncomeAsyn({'startTime':exchange.parse8601('2023-12-01T00:00:00'),'endTime':exchange.parse8601('2024-05-05T00:00:00')})
#urls = exchange.fapiPrivateGetIncomeAsynId({'downloadId':'839850042831552512'})
#'url': ''

def all_trade_history(df):
    start_ = df.iloc[0]['timestamp']

    balance = exchange.fetch_balance()
    trade_symbols = balance['info']['positions']
    symbols = []
    for trade_symbol in trade_symbols:
        if float(trade_symbol['updateTime']) != 0:
            symbols.append(trade_symbol['symbol'])

    day = 24 * 60 * 60 * 1000
    end_ = df.iloc[-1]['timestamp']
    all_trades = []

    for sym in symbols:
        start_time = start_
        while start_time < end_:

            end_time = start_time + day

            trades = exchange.fetch_my_trades (sym,start_time, None, {
                'endTime': end_time,
            })
            if len(trades):
                last_trade = trades[len(trades) - 1]
                start_time = last_trade['timestamp'] + 1
                all_trades = all_trades + trades
            else:
                start_time = end_time

    return all_trades

def arrangement_trade_history(all_trades):
    trade_history = []
    date_time,amount,realizedPnl,fee, side,trade_price = 0,0,0,0,0,0

    i = 0
    while i < len(all_trades):
        if float( all_trades[i]['info']['realizedPnl']) == 0:
            amount , realizedPnl ,fee, trade_price,cost = 0,0,0,0,0
            while i < len(all_trades) and float(all_trades[i]['info']['realizedPnl']) == 0:
                date_time =  all_trades[i]['datetime']
                date_timestamp = all_trades[i]['timestamp']
                symbol = all_trades[i]['info']['symbol']
                amount += float( all_trades[i]['amount'])
                cost += float( all_trades[i]['cost'])
                realizedPnl += float( all_trades[i]['info']['realizedPnl'])
                fee += float( all_trades[i]['fee']['cost'])
                side =  all_trades[i]['info']['side']
                trade_price +=  float( all_trades[i]['amount']) * float(all_trades[i]['info']['price'])
                i += 1
            trade_history.append({'symbol':symbol,'timestamp':date_timestamp,'amount':round(amount,3),'pnl':realizedPnl,'fee':fee,'side':side,'price':round(trade_price/amount,2),'cost':cost})
        elif float( all_trades[i]['info']['realizedPnl']) != 0:
            amount , realizedPnl ,fee, trade_price,cost = 0,0,0,0,0
            while i < len(all_trades) and float(all_trades[i]['info']['realizedPnl']) != 0:
                date_time =  all_trades[i]['datetime']
                date_timestamp = all_trades[i]['timestamp']
                symbol = all_trades[i]['info']['symbol']
                amount += float( all_trades[i]['amount'])
                cost += float( all_trades[i]['cost'])
                realizedPnl +=  float( all_trades[i]['info']['realizedPnl'])
                fee += float( all_trades[i]['fee']['cost'])
                side =  all_trades[i]['info']['side']
                trade_price +=  float( all_trades[i]['amount']) * float(all_trades[i]['info']['price'])
                i += 1
            trade_history.append({'symbol':symbol,'timestamp':date_timestamp,'amount':round(amount,3),'pnl':realizedPnl,'fee':fee,'side':side,'price':round(trade_price/amount,2),'cost':cost})

    trade_history = sorted(trade_history,key=itemgetter('timestamp'))

    return trade_history

def trade_to_position_history(trade_history, all_fundings, all_transfers , all_liquidations):

    df = pd.DataFrame(columns =[
                                'crypto_id',
                                'symbol',
                                'open_time',
                                'close_time',
                                'open_timestamp',
                                'close_timestamp',
                                'side',
                                'leverage',
                                'open_amount',
                                'close_amount',
                                'open_price',
                                'close_price',
                                'open_cost',
                                'close_cost',
                                'tp',
                                'sl',
                                'open_commission_fee',
                                'close_commission_fee',
                                'funding_fee',
                                'insurance_clear',
                                'realized_pnl',
                                'pnl',
                                'pnl_percentage',
                                'open_balance',
                                'close_balance',
                                ])

    for _ in range(len(trade_history)//2):
        funding_fee,liquidation_fee = 0,0

        enter_cost = float(trade_history[2 * _]['cost'])
        enter_price = float(trade_history[2 * _]['price'])
        enter_timestamp = int(trade_history[2 * _]['timestamp'])
        enter_datetime = datetime.fromtimestamp(enter_timestamp/1000)
        enter_amount = float(trade_history[2 * _]['amount'])

        exit_cost = float(trade_history[2 * _+1]['cost'])
        exit_price = float(trade_history[2 * _+1]['price'])
        exit_timestamp = int(trade_history[2 * _+1]['timestamp'])
        exit_datetime = datetime.fromtimestamp(exit_timestamp/1000)
        exit_amount = float(trade_history[2 * _ + 1]['amount'])

        coin_symbol = trade_history[2 * _]['symbol']
        balance = 0
        for a in range(len(all_transfers)):
            if _ == 0:
                if all_transfers.iloc[a]['timestamp'] < exit_timestamp:
                    balance = all_transfers.iloc[a]['Amount']
            else:
                if all_transfers.iloc[a]['timestamp'] < exit_timestamp and all_transfers.iloc[a]['timestamp'] > trade_history[2 * _ - 1]['timestamp']:
                    balance = all_transfers.iloc[a]['Amount']


        enter_side = trade_history[2 * _]['side']
        if enter_side == 'BUY':
            enter_side = 'long'
        else:
            enter_side = 'short'

        open_fee = float(trade_history[2 * _]['fee'])
        close_fee = float(trade_history[2 * _ + 1]['fee'])

        fee = open_fee+close_fee

        for b in range(len(all_fundings)):
            if all_fundings.iloc[b]['timestamp'] >= enter_timestamp and all_fundings.iloc[b]['timestamp'] <= exit_timestamp:
                funding_fee -= all_fundings.iloc[b]['Amount']

        for c in range(len(all_liquidations)):
            if all_liquidations.iloc[c]['timestamp'] >= enter_timestamp and all_liquidations.iloc[c]['timestamp'] <= exit_timestamp:
                liquidation_fee -= all_liquidations.iloc[c]['Amount']

        pnl = float(trade_history[2 * _+1]['pnl'])
        new_data ={'crypto_id':int(crypto_id),
                   'symbol':coin_symbol,
                   'open_time': enter_datetime,
                   'close_time': exit_datetime,
                   'open_timestamp':enter_timestamp,
                   'close_timestamp':exit_timestamp,
                   'side': enter_side,
                   'leverage': None,
                   'open_amount':enter_amount,
                   'close_amount': exit_amount,
                   'open_price': enter_price,
                   'close_price': exit_price,
                   'open_cost': enter_cost,
                   'close_cost': exit_cost,
                   'tp':None,
                   'sl':None,
                   'open_commission_fee': open_fee,
                   'close_commission_fee': close_fee,
                   'funding_fee': funding_fee,
                   'insurance_clear': liquidation_fee,
                   'realized_pnl': pnl,
                   'pnl': pnl - fee - funding_fee - liquidation_fee,
                   'pnl_percentage': None,
                   'open_balance':balance,
                   'close_balance':0,
                   }
        df2 = pd.DataFrame(new_data,index=[_])
        df = pd.concat([df,df2])

    return df

def update_information(df):
    for _ in range(len(df)):
        if _ == 0:
            df.at[df.index[_], 'close_balance'] = df.iloc[_]['open_balance'] + df.iloc[_]['pnl']
            df.at[df.index[_], 'pnl_percentage'] = ((df.iloc[_]['close_balance']-df.iloc[_]['open_balance'])/df.iloc[_]['open_balance'])*100
        else:
            df.at[df.index[_], 'open_balance'] = df.iloc[_ - 1]['close_balance'] + df.iloc[_]['open_balance']
            df.at[df.index[_], 'close_balance'] = df.iloc[_]['open_balance'] + df.iloc[_]['pnl']
            df.at[df.index[_], 'pnl_percentage'] = ((df.iloc[_]['close_balance']-df.iloc[_]['open_balance'])/df.iloc[_]['open_balance'])*100

    return df

def save_database(df):
    MYSQL_HOSTNAME = 'localhost' # you probably don't need to change this
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '!taewonb916'
    MYSQL_DATABASE = 'mysite'

    connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
    # connect_args = {'ssl': {'ca': '/content/rds-ca-2015-root.pem'}}

    db_connection = create_engine(connection_string)

#SELECT COUNT(*) as cnt FROM pybo_tradehistory;
    df.to_sql(name='pybo_tradehistory', con=db_connection, if_exists='append',index=False)

def check_blank_database():
    db = pymysql.connect(
        host='localhost',            # 접속할 mysql server의 주소
        port=3306,        # 접속할 mysql server의 포트 번호
        user='root',     
        passwd='!taewonb916',
        db='mysite'         # 접속할 database명
    )

    cursor = db.cursor()

    result = cursor.excute("SELECT COUNT(*) as cnt FROM pybo_tradehistory;")
    len_ = result.fetchall()

    print(len_)
    return len_

def main():
    path_ = "/root/mysite/media/"
    if user not in os.listdir(path_):
        os.system("mkdir "+ path_ + user)

    if api_key not in os.listdir(path_ + user + "/"):
        os.system("mkdir "+ path_ + user + "/" + api_key)

        path = path_ + user + "/" + api_key+ "/"
        if len(os.listdir(path)) == 0:
            urls, file_name = get_transaction()
            download(urls, file_name, path)
            unzip(path, file_name)


    check = check_blank_database()

    if check == 0:
        path = f"/root/mysite/media/{user}/{api_key}/"

        all_data, funding, transfer, liquidation = csv_to_dataframe(path)
        all_trade = all_trade_history(all_data)
        arrangement_trade = arrangement_trade_history(all_trade)
        position = trade_to_position_history(arrangement_trade, funding, transfer, liquidation)
        data = update_information(position)
        save_database(data)
    print('end')

if __name__ == '__main__':
    main()
