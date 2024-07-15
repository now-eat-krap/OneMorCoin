from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('update/<int:pk>/', views.crypto_update, name='update'),
    path('create/', views.crypto_create, name='create'),
    path('create/setting', views.crypto_setting, name='setting'),
    path('delete/<int:pk>/', views.crypto_delete, name='delete'),
]

