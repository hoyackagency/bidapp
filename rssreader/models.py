from django.db import models

class FeedEntry(models.Model):
    title = models.CharField(max_length=1000)
    link = models.URLField()
    published_date = models.DateTimeField()
    content = models.TextField()
    pay_range = models.CharField(max_length=255, null=True, blank=True)
    job_type = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    skills = models.CharField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    feed = models.ForeignKey('RSSFeed', on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class RSSFeed(models.Model):
    feed_name = models.CharField(max_length=255)
    url = models.URLField(max_length=500)  # Set the max_length to 500 characters
    description = models.TextField(default='')
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.feed_name


