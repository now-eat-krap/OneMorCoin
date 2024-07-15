from django import forms
from .models import EconomicCalendar, News

class EconomicCalendarForm(forms.ModelForm):
    class Meta:
        model = EconomicCalendar
        fields = ['scheduled_time','contents']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['post_date','news_link','title','img_link']
