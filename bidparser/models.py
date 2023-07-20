from django.db import models
from rssreader.models import FeedEntry, RSSFeed

class Job(models.Model):
    feed_entry = models.OneToOneField(FeedEntry, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('accept', 'Accept'), ('decline', 'Decline'), ('recycle', 'Recycle')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job for: {self.feed_entry.title}"
    
class Bid(models.Model):
    bid_entry = models.OneToOneField(Job, on_delete=models.CASCADE)
    description = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid for: {self.bid_entry.title}"

class Prompt(models.Model):
    prompt_feed = models.OneToOneField(RSSFeed, on_delete=models.CASCADE)
    prompt_header = models.TextField(default='')
    prompt_body = models.TextField(default='')
    prompt_footer = models.TextField(default='')
    enabled = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prompt for: {self.prompt_feed.title}"