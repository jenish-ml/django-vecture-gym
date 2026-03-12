from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products_list, name='products_list'),
    path('trainers/', views.trainers_list, name='trainers_list'),
    path('trainers/<int:pk>/', views.trainer_detail, name='trainer_detail'),
    path('contact/', views.contact, name='contact'),
]
