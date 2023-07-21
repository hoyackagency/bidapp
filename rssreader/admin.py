from django.contrib import admin
from .models import FeedEntry, RSSFeed

class FeedEntryAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(archived=False)

admin.site.register(FeedEntry, FeedEntryAdmin)
admin.site.register(RSSFeed)