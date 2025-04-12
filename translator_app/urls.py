from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('translate/', views.ajax_translate, name='ajax_translate'),
    path('suggestions/', views.ajax_suggestions, name='ajax_suggestions'),
]
