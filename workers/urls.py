from django.urls import path

from . import views

urlpatterns = [
    path('', views.worker_list_view, name='worker_list'),
    path('create/', views.worker_create_view, name='worker_create'),
    path('edit/<int:pk>', views.worker_update_view, name='worker_edit'),
    path('delete/<int:pk>', views.worker_delete_view, name='worker_delete'),
]