from django.urls import path

from . import views

app_name = 'exercises'

urlpatterns = [
    path('<slug:slug>/', views.get_exercise, name='get-exercise'),
]
