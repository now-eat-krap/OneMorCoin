from django.contrib.auth import authenticate, login, logout,get_user_model
from django.shortcuts import render, redirect, get_object_or_404
#from account.forms import UserCreationForm
from .forms import UserCreationForm,UserChangeForm, CryptoForm
from .models import Crypto, User
import os
import subprocess
from django.contrib import messages
import ccxt
import time
import sys
sys.path.append("/root/mysite/account/function")
from download_trasaction_history_binance import *
from trade_history_from_csv_binance import *

def logout_view(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            nickname = form.cleaned_data.get('nickname')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email,nickname=nickname, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

def detail(request,pk):
    User = get_user_model()
    user = get_object_or_404(User,pk=pk)
    crypto_list = Crypto.objects.values().filter(user_id=pk)
    context = {
        'user': user,
        'crypto_list':crypto_list
    }
    return render(request, 'account/detail.html', context)

def crypto_update(request,pk):
    crypto = get_object_or_404(Crypto, pk=pk)
    if request.method == 'POST':
        form = CryptoForm(request.POST,instance=crypto)
        if form.is_valid():
            form.save()
            return redirect('account:detail', request.user.pk)
    else:
        form = CryptoForm(instance=crypto)
    context = {
        'form':form
    }
    return render(request, 'account/update.html', context)

def crypto_setting(request):
    user = get_object_or_404(User, pk=request.user.pk)
    crypto_currency = request.GET['crypto_currency']
    api_name = request.GET['api_name']
    api_key = request.GET['api_key']
    api_secret = request.GET['api_secret']

    crypto = Crypto(user=user, crypto_currency=crypto_currency, api_name=api_name, api_key=api_key, api_secret=api_secret)
    crypto.save()
    crypto_id = Crypto.objects.filter(api_key=api_key).values('id')
    crypto_id = crypto_id[0]['id']

    if crypto_currency == "binance":
        exchange = connect(api_key, api_secret)
        path_ = "/root/mysite/media/"
        if str(user) not in os.listdir(path_):
            os.system("mkdir "+ path_ + str(user))
        else:
            pass

        if api_key not in os.listdir(path_ + str(user) + "/"):
            os.system("mkdir "+ path_ + str(user) + "/" + api_key)
            path = path_ + str(user) + "/" + api_key+ "/"
            if len(os.listdir(path)) == 0:
                urls, file_name = get_transaction(exchange)
                download(urls, file_name, path)
                unzip(path, file_name)
        else:
            pass

        check = check_blank_database()

        if check == 0:
            path = f"/root/mysite/media/{str(user)}/{api_key}/"
            all_data, funding, transfer, liquidation = csv_to_dataframe(path)
            all_trade = all_trade_history(exchange,all_data)
            arrangement_trade = arrangement_trade_history(all_trade)
            position = trade_to_position_history(crypto_id,arrangement_trade, funding, transfer, liquidation)
            data = update_information(position)
            save_database(data)
        else:
            pass

    return render(request,'account/detail.html')

def crypto_create(request):

    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.pk)
        currency = request.POST.get('crypto_currency')
        key = request.POST.get('api_key')
        secret = request.POST.get('api_secret')

        try:
            if currency == "binance":
                exchange = ccxt.binance(config={
                    'apiKey': key,
                    'secret': secret,
                    'enableRateLimit': True,
                    'options': {
                        'defaultType': 'future'
                    }
                })
            elif currency == "bybit":
                exchange = ccxt.bybit(config={
                    'apiKey': key,
                    'secret': secret,
                    'enableRateLimit': True,
                })

            exchange.load_markets()

            #crypto = Crypto(user=user, crypto_currency=request.POST.get('crypto_currency'), api_name=request.POST.get('api_name'), api_key=request.POST.get('api_key'), api_secret=request.POST.get('api_secret'))
            #crypto.save()
            #crypto_currency = request.POST.get('crypto_currency')
            #api_name = request.POST.get('api_name')
            #api_key = request.POST.get('api_key')
            #api_secret = request.POST.get('api_secret')
            #crypto_id = Crypto.objects.filter(api_key=api_key).values('id')
            #crypto_id = crypto_id[0]['id']
            #print("end",crypto_id)
            #os.system(f"python /root/mysite/function/{crypto_currency}/trade_history.py -user {user} -crypto_currency {crypto_currency} -api_name {api_name} -api_key {api_key} -api_secret {api_secret} -crypto_id {crypto_id} &")
            #os.system(f"python /root/mysite/function/{crypto_currency}/download_trasaction_history.py -user {user} -crypto_currency {crypto_currency} -api_name {api_name} -api_key {api_key} -api_secret {api_secret} &")
            #os.system('wait')
            #os.system(f"python /root/mysite/function/{crypto_currency}/trade_history_from_csv.py -user {user} -crypto_currency {crypto_currency} -api_name {api_name} -api_key {api_key} -api_secret {api_secret} -crypto_id {crypto_id} &")
        except:
            messages.add_message(request,messages.ERROR, 'Fill Blank or Check API Key, API Secret')
            return render(request,'account/create.html')

        return redirect('account:detail', user.pk)

    return render(request,'account/create.html')

def crypto_delete(request,pk):
    crypto = get_object_or_404(Crypto,user_id = request.user.pk ,pk=pk)
    if request.user != crypto.user:
        messages.error(request, '삭제권한이 없습니다')
    else:
        crypto.delete()
    return redirect('account:detail',request.user.pk)
