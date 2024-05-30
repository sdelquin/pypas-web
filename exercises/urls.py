from django.urls import path

from . import views

app_name = 'exercises'

urlpatterns = [
    path('<slug:slug>/get/', views.get_exercise, name='get-exercise'),
    path('<slug:slug>/put/', views.put_exercise, name='put-exercise'),
]
