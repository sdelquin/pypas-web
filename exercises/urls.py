from django.urls import path

from . import views

app_name = 'exercises'

urlpatterns = [
    path('get/<slug:slug>/', views.get, name='get'),
    path('list/', views.list, name='list'),
]
