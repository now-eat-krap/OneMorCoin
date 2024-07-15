from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse

from .forms import TradeHistory
from .models import TradeHistory
from account.models import Crypto
from account.forms import CryptoForm

from datetime import datetime
import time
import ccxt
import pprint

import sys
sys.path.append("/root/mysite/analysis/")
from open_positions import *

def open_positions(request):
    return render(request, 'analysis/open_positions.html')

def live_positions(request):
    response_data = {"info":[]}
    crypto_lists = Crypto.objects.values().filter(user_id=request.user.pk)
    for crypto_list in crypto_lists:
        exchange = connect(crypto_list['crypto_currency'],crypto_list['api_key'],crypto_list['api_secret'])
        response_data = get_open_positions(exchange,response_data,crypto_list['crypto_currency'],crypto_list['api_name'])

    return JsonResponse(response_data)

def summary(request):
    crypto_list = Crypto.objects.values().filter(user_id=request.user.pk)
    context = {
        'crypto_list':crypto_list,
    }

    return render(request, 'analysis/summary.html',context)

def trade(request):
    entry_url=request.GET['url_catch']
    return render(request, 'analysis/trade_history.html')

def trade_history(request):
    crypto_list = Crypto.objects.values().filter(user_id=request.user.pk)
    trade_history_list = TradeHistory.objects.values().filter(crypto_id = crypto_list[0]['id'])
    trade_coin_list = list(trade_history_list.values('symbol'))
    trade_coin_list = list({v['symbol']:v for v in trade_coin_list}.values())

    if len(trade_history_list)!=0:
        all_start_end_date=[str(trade_history_list[0]['open_time']), str(trade_history_list[len(trade_history_list)-1]['open_time'])]
    else:
        all_start_end_date=list()

    if request.method == 'POST':
        if request.POST.get('start_date') != None and request.POST.get('end_date') != None:
            start_end_date = [request.POST.get('start_date'),request.POST.get('end_date')]
            start_date = datetime.strptime(start_end_date[0]+" 00:00:00.0000", '%Y-%m-%d %H:%M:%S.%f')
            end_date = datetime.strptime(start_end_date[1]+" 00:00:00.0000", '%Y-%m-%d %H:%M:%S.%f')
            trade_history_list = trade_history_list.values().filter(open_time__gte = start_date).filter(close_time__lte = end_date)
        else:
            start_end_date=list()
        context = {
            'crypto_list':crypto_list,
            'trade_history_list ':trade_history_list,
            'all_start_end_date':all_start_end_date,
            'start_end_date':start_end_date,
            'trade_coin_list':trade_coin_list,
            'select_id':int(request.POST.get('crypto_currency'))
        }
        return render(request, 'analysis/trade_history.html', context)
    else:
        form = CryptoForm()
    context = {
        'form':form,
        "crypto_list":crypto_list,
        'trade_history_list ':trade_history_list,
        'all_start_end_date':all_start_end_date,
        'start_end_date':list(),
        'select_id':request.POST.get('crypto_currency')
    }
    return render(request, 'analysis/trade_history.html',context)

def pnl(request):
    crypto_list = Crypto.objects.values().filter(user_id=request.user.pk)
    context = {
        'crypto_list':crypto_list,
    }

    return render(request, 'analysis/pnl.html',context)

