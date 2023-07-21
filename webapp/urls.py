# myproject/webapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('thumbsdown/', views.thumbs_down, name='thumbs_down'),
]
