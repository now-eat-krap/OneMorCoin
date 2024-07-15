from django.urls import path

from . import views

app_name = 'trading_journal'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.trading_journal, name='trading_journal'),
    path('<int:pk>/create/', views.create_journal, name='create'),
]
