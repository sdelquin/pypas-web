from django.urls import path

from . import views

app_name = 'exercises-admin'

urlpatterns = [
    path('add-exercises-to-frame/', views.add_exercises_to_frame, name='add-exercises-to-frame'),
]
