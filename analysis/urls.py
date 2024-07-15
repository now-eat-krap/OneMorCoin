from django.urls import path

from . import views

app_name = 'analysis'

urlpatterns = [
    path('open_positions',views.open_positions, name='open_positions'),
    path('open_positions/live',views.live_positions, name='live_positions'),
    path('summary',views.summary, name='summary'),
    path('trade_history',views.trade_history, name='trade_history'),
    path('pnl',views.pnl, name='pnl'),
    #path('trade_history/trade/',views.trade, name='trade')
]
