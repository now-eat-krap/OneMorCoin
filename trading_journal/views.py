from django.shortcuts import render
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

def home(request):
    return render(request, 'trading_journal/home.html')

def trading_journal(request,pk):

    return render(request, 'trading_journal/trading_journal.html')

def create_journal(request,pk):
    currency = None
    symbol = None
    analysis_time = None
    if request.method == "POST":
        currency = (request.POST.get('crypto_currency')).upper()
        symbol = request.POST.get('symbol')
        analysis_time = request.POST.getlist('analysis_time')

        candle_content = [request.POST.get('content_1M'), request.POST.get('content_1W'), request.POST.get('content_1D'), request.POST.get('content_4H'), request.POST.get('content_1H'), request.POST.get('content_15m')]

        transaction_content = request.POST.get('transaction_content')
        entry_price = request.POST.get('entry_price')
        tp = request.POST.get('tp')
        sl = request.POST.get('sl')
        amount = request.POST.get('amount')

        img_content = [request.FILES.getlist('img_1M'), request.FILES.getlist('img_1W'), request.FILES.getlist('img_1D'), request.FILES.getlist('img_4H'), request.FILES.getlist('img_1H'), request.FILES.getlist('img_15m')]

        #form = AnswerForm(request.POST)
        #if form.is_valid():
        #    answer = form.save(commit=False)
        #    answer.create_date = timezone.now()
        #    answer.question = question
        #    answer.save()
        #    return redirect(':detail', question_id=question.id)
    #else:
    #    return render(request, 'trading_journal/create.html')

    context = {
               'currency': currency,
               'symbol': symbol,
               'analysis_time': analysis_time,
              }
    
    return render(request, 'trading_journal/create.html', context)
