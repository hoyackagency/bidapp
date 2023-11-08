from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_list_view, name='feed_list'),
    path('<int:feed_id>/', views.feed_detail_view, name='feed_detail'),
]
