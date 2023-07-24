# rssreader/serializers.py
from rest_framework import serializers
from .models import FeedEntry, RSSFeed

class RSSFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSSFeed
        fields = '__all__'

class FeedEntrySerializer(serializers.ModelSerializer):
    feed = RSSFeedSerializer()

    class Meta:
        model = FeedEntry
        fields = '__all__'  # or list all the fields you need