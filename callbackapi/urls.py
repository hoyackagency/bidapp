from django.urls import path
from . import views

urlpatterns = [
    path('worker/cb', views.worker_callback, name='worker_callback'),
    path('result/cb', views.bid_result_callback, name="bid_result_callback"),
]