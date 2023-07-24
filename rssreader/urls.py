from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import FeedEntryViewSet, RSSFeedViewSet, parse_rss_feed_view

router = DefaultRouter()
router.register(r'feed-entries', FeedEntryViewSet)
router.register(r'rss-feeds', RSSFeedViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('parse/', parse_rss_feed_view, name='parse'),
]
