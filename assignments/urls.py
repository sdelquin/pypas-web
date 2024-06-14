from django.urls import path

from . import views

app_name = 'assignments'

urlpatterns = [
    path('<slug:exercise_slug>/upload/', views.upload, name='upload'),
    path('stats/', views.stats, name='stats'),
]
