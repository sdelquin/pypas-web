from django.urls import path

from . import views

app_name = 'exercises'

urlpatterns = [
    path('get/<slug:slug>/', views.get, name='get'),
    path('info/<slug:slug>/', views.info, name='info'),
    path('list/', views.list, name='list'),
]
