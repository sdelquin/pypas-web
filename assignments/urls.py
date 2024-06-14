from django.urls import path

from . import views

app_name = 'assignments'

urlpatterns = [
    path('<slug:exercise_slug>/put/', views.put, name='put'),
    path('stats/', views.stats, name='stats'),
]
