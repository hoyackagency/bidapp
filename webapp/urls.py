# myproject/webapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('thumbs/', views.thumbs_updown, name='thumbs_updown'),
]
