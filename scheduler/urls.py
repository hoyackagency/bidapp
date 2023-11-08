from django.urls import path
from .views import do_schedule

urlpatterns = [
    path('', do_schedule, name='write_bids'),
]
