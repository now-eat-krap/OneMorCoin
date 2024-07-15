import ccxt
from datetime import datetime

def connect(crypto_currency,api_key,api_secret):
    api_key = api_key
    secret = api_secret

    if crypto_currency == "binance":

        exchange = ccxt.binance(config={
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
        })
    elif crypto_currency == "bybit":
        exchange = ccxt.bybit(config={
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
        })

    return exchange

def trade_start_date(exchange):
    exchange.load_markets()
    sym = (exchange.fetchClosedOrders())[0]['symbol']
    fetch_position = exchange.fetchPosition(sym)
    trade_start_timestamp = int(fetch_position['info']['createdTime'])
    dt = datetime.fromtimestamp(trade_start_timestamp//1000)
    trade_start_date = dt.date()

    return trade_start_date
