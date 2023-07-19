from .rss_parser import parse_rss_feed
from django.http import JsonResponse

def parse_rss_feed_view(request):
    parse_rss_feed(request)
    data = {'message': "RSS feed parsing initiated successfully"}
    return JsonResponse(data)
