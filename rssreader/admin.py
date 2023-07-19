from django.contrib import admin
from .models import FeedEntry
from .models import RSSFeed

admin.site.register(FeedEntry)
admin.site.register(RSSFeed)
