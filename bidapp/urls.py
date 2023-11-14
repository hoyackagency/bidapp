"""bidapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rssreader.views import parse_rss_feed_view
from jobs.apiviews import FeedEntryView, JobsView, JobViewSet
from rest_framework.routers import DefaultRouter
from feeds.views import feed_list_view

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='jobs')

urlpatterns = [
    path('', feed_list_view, name='home'),
    path('admin/', admin.site.urls),
    path('parse-feed/', parse_rss_feed_view, name='parse_rss_feed'),
    path('worker/', include('workers.urls')),
    path('rssreader/', include('rssreader.urls')),
    path('view/', FeedEntryView.as_view(), name='view_feed_entry'),
    path('jobs/', include('jobs.urls')),
    path('feeds/', include('feeds.urls')),
    path('scheduler/', include('scheduler.urls')),
    path('cb/', include('callbackapi.urls'))
]

urlpatterns += router.urls