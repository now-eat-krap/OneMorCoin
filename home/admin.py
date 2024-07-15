from django.contrib import admin

from .forms import EconomicCalendarForm, NewsForm
from .models import EconomicCalendar, News

class EconomicCalendarAdmin(admin.ModelAdmin):
    list_display = ('scheduled_time','contents',)
    search_fields = ('scheduled_time','contetns',)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('post_date','news_link','title','img_link')
    search_fiels = ('post_date','news_link','title','img_link')

admin.site.register(EconomicCalendar, EconomicCalendarAdmin)
admin.site.register(News, NewsAdmin)
