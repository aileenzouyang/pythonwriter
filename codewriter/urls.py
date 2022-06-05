from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.upload, name='upload'),
    path('accounts/load', views.table, name='load'),
    path('load', views.table, name='load'),
    path('contact', views.contact, name='contact'),
    path('remove', views.remove, name='remove'),
    path('evaluate', views.evaluate, name='evaluate'),
    path('removecolumns', views.removecolumns, name='removecolumns')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)