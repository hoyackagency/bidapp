from rest_framework import viewsets
from .models import FeedEntry, RSSFeed
from .rss_parser import parse_rss_feed
from .serializers import FeedEntrySerializer, RSSFeedSerializer
from django.http import JsonResponse

class FeedEntryViewSet(viewsets.ModelViewSet):
    queryset = FeedEntry.objects.all()
    serializer_class = FeedEntrySerializer

class RSSFeedViewSet(viewsets.ModelViewSet):
    queryset = RSSFeed.objects.all()
    serializer_class = RSSFeedSerializer

def parse_rss_feed_view(request):
    parse_rss_feed(request)
    data = {'message': "RSS feed parsing initiated successfully"}
    return JsonResponse(data)
