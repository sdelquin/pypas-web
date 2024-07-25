from django.urls import path

from . import views

app_name = 'assignments'

urlpatterns = [
    path('put/<slug:exercise_slug>/', views.put, name='put'),
    path('log/', views.log, name='log'),
    path('log/verbose/', views.log, dict(verbose=True), name='log-verbose'),
]
