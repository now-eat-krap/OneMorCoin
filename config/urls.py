from django.contrib import admin
from django.urls import path, include
from home import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('account/', include('account.urls')),
    path('', views.index, name='index'),  # '/' 에 해당되는 path
    path('analysis/', include('analysis.urls')),
    path('trading_journal/',include('trading_journal.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
