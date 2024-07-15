import ccxt
import pprint

def connect(crypto_currency, api_key, api_secret):
    if crypto_currency == 'binance':
        exchange = ccxt.binance(config={
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            }
        })
    elif crypto_currency == 'bybit':
        exchange = ccxt.bybit(config={
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            }
        })

    return exchange

def get_open_positions(exchange,response_data,crypto_currency,api_name):
    positions = exchange.fetch_positions()
    #pprint.pprint(positions)
    for position in positions:
        percentage = position['percentage']
        if position['percentage'] == None:
            percentage = ((position['markPrice']-position['entryPrice'])/position['entryPrice'])*100
        try:
            margin_type = (position['marginType']).title()
        except:
            margin_type = (position['marginMode']).title()

        response_data["info"].append({
                                "crypto_currency": crypto_currency,
                                "api_name": api_name,
                                "symbol":position['info']['symbol'],
                                "leverage":position['leverage'],
                                "side":(position['side']).title(),
                                "position_size":position['contracts'],
                                "entry_price":position['entryPrice'],
                                "market_price":round(position['markPrice'],2),
                                "liquidation_price":round(position['liquidationPrice'],2),
                                "percentage":str(round(percentage,2))+" %",
                                "unrealized_pnl":round(position['unrealizedPnl'],2),
                                "margin_type":margin_type,
                               })

    return response_data

""" binance
[{'collateral': 4.10449107,
  'contractSize': 1.0,
  'contracts': 0.001,
  'datetime': '2024-06-04T13:55:41.069Z',
  'entryPrice': 69000.0,
  'hedged': False,
  'id': None,
  'info': {'adlQuantile': '2',
           'breakEvenPrice': '45074.36',
           'entryPrice': '69000.0',
           'isAutoAddMargin': 'false',
           'isolated': True,
           'isolatedMargin': '4.10449107',
           'isolatedWallet': '3.43620000',
           'leverage': '20',
           'liquidationPrice': '65827.10843373',
           'marginType': 'isolated',
           'markPrice': '69668.29107801',
           'maxNotionalValue': '100000000',
           'notional': '69.66829107',
           'positionAmt': '0.001',
           'positionSide': 'BOTH',
           'symbol': 'BTCUSDT',
           'unRealizedProfit': '0.66829107',
           'updateTime': '1717509341069'},
  'initialMargin': 3.48341455,
  'initialMarginPercentage': 0.05,
  'leverage': 20.0,
  'liquidationPrice': 65827.10843373,
  'maintenanceMargin': 0.27867316428,
  'maintenanceMarginPercentage': 0.004,
  'marginMode': 'isolated',
  'marginRatio': 0.0679,
  'marginType': 'isolated',
  'markPrice': 69668.29107801,
  'notional': 69.66829107,
  'percentage': 19.18,
  'side': 'long',
  'stopLossPrice': None,
  'symbol': 'BTC/USDT:USDT',
  'takeProfitPrice': None,
  'timestamp': 1717509341069,
  'unrealizedPnl': 0.66829107}]
"""

""" bybit
[{'collateral': 192.79835093,
  'contractSize': 1.0,
  'contracts': 0.15,
  'datetime': '2024-06-04T08:00:00.820Z',
  'entryPrice': 3851.73,
  'id': None,
  'info': {'adlRankIndicator': '2',
           'autoAddMargin': '0',
           'avgPrice': '3851.73',
           'bustPrice': '2567.82',
           'createdTime': '1711710352416',
           'cumRealisedPnl': '35.45460196',
           'curRealisedPnl': '-0.2857299',
           'isReduceOnly': False,
           'leverage': '3',
           'leverageSysUpdatedTime': '',
           'liqPrice': '2587.08',
           'markPrice': '3783.14',
           'mmrSysUpdatedTime': '',
           'positionBalance': '192.79835093',
           'positionIM': '5.777595',
           'positionIdx': '0',
           'positionMM': '1.925865',
           'positionStatus': 'Normal',
           'positionValue': '577.7595',
           'riskId': '11',
           'riskLimitValue': '900000',
           'seq': '139531867637',
           'sessionAvgPrice': '',
           'side': 'Buy',
           'size': '0.15',
           'stopLoss': '0.00',
           'symbol': 'ETHUSDT',
           'takeProfit': '0.00',
           'tpslMode': 'Full',
           'tradeMode': '1',
           'trailingStop': '0.00',
           'unrealisedPnl': '-10.2885',
           'updatedTime': '1717488000820'},
  'initialMargin': 192.5865,
  'initialMarginPercentage': 0.3333333333333333,
  'lastPrice': None,
  'lastUpdateTimestamp': None,
  'leverage': 3.0,
  'liquidationPrice': 2587.08,
  'maintenanceMargin': 2.889,
  'maintenanceMarginPercentage': 0.005000350491856905,
  'marginMode': 'isolated',
  'marginRatio': 0.0149,
  'markPrice': 3783.14,
  'notional': 577.7595,
  'percentage': None,
  'side': 'long',
  'stopLossPrice': 0.0,
  'symbol': 'ETH/USDT:USDT',
  'takeProfitPrice': 0.0,
  'timestamp': 1717488000820,
  'unrealizedPnl': -10.2885}]
"""
