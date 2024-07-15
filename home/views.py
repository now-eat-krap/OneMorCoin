from django.shortcuts import render

from .forms import EconomicCalendarForm, NewsForm
from .models import EconomicCalendar, News
from datetime import datetime, timedelta, time
from dateutil.relativedelta import *
import pprint

# Create your views here.
def economic_information():
    today = datetime.now().date()
    #data = EconomicCalendar.objects.values().all()
    monday = today + relativedelta(weekday=MO(-1))
    data = EconomicCalendar.objects.filter(scheduled_time__range=(monday,monday+timedelta(days=7))).values().all()
    week = [monday+timedelta(i) for i in range(7)]

    news = News.objects.all().order_by('-post_date').filter(post_date__range=(today,today+timedelta(days=1))).values()

    context = {
        'calendar_lists': data,
        'week': week,
        'today': today,
        'news': news,
    }
    return context

def index(request):
    context = economic_information()

    return render(request, 'home/home.html', context)
