from django.urls import path

from . import views

app_name = 'access'

urlpatterns = [
    path('auth/<slug:token>/', views.authenticate_user, name='authenticate-user'),
]
