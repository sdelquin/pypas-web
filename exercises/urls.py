from django.urls import path

from . import views

app_name = 'exercises'

urlpatterns = [
    path('<slug:slug>/get/', views.get, name='get'),
]
