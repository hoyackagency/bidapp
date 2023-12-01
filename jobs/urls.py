from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('archived/', views.job_archived_list_view, name='job_archived_list'),
    path('<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('<int:job_id>/archive', views.job_archive_view, name='job_archive'),
]
