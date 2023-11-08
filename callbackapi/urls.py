from django.urls import path
from . import views

urlpatterns = [
    # path('workers/cb', views.worker_callback, name='worker_callback'),
    path('data/cb', views.bid_result_callback, name="bid_result_callback"),
]