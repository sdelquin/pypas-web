from django.urls import path

from . import views

app_name = 'assignments'

urlpatterns = [
    path('stats/', views.stats, name='stats'),
]
