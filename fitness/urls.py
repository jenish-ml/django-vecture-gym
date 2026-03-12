from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
    path('update-progress/', views.update_progress, name='update_progress'),
]
