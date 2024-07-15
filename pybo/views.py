from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import QuestionForm, AnswerForm
from .models import Question

from pybo.trade import *

from datetime import datetime
import time

def qna(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

#def trade(request):
#    entry_url=request.GET['url_catch']
#    print("Hello",entry_url)
#    return render(request, 'pybo/trade_history.html')

#def trade_history(request):
#    crypto_list = Crypto.objects.values().filter(user_id=request.user.pk)
#    trade_history_list = TradeHistory.objects.values().filter(crypto_id = crypto_list[0]['id'])
#    if len(trade_history_list)!=0:
#        start_end_date=[str(trade_history_list[0]['open_time']), str(trade_history_list[len(trade_history_list)-1]['open_time'])]
#    else:
#        start_end_date=list()

#    if request.method == 'POST':
#        start_end_date = [request.POST.get('start_date'),request.POST.get('end_date')]
#        start_date = datetime.strptime(start_end_date[0]+" 00:00:00.0000", '%Y-%m-%d %H:%M:%S.%f')
#        end_date = datetime.strptime(start_end_date[1]+" 00:00:00.0000", '%Y-%m-%d %H:%M:%S.%f')
#        trade_history_list = trade_history_list.values().filter(open_time__gte = start_date).filter(close_time__lte = end_date)
#        context = {
#            'crypto_list':crypto_list,
#            'trade_history_list ':trade_history_list ,
#            'start_end_date':start_end_date,
#            'select_id':int(request.POST.get('crypto_currency'))
#        }
#        return render(request, 'pybo/trade_history.html', context)
#    else:
#        form = CryptoForm()
#    context = {
#        'form':form,
#        "crypto_list":crypto_list,
#        'start_end_date':start_end_date,
#    }
#    return render(request, 'pybo/trade_history.html',context)
