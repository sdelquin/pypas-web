from django.urls import path

from . import views

app_name = 'chunks-admin'

urlpatterns = [
    path('add-chunks-to-frame/', views.add_chunks_to_frame, name='add-chunks-to-frame'),
]
