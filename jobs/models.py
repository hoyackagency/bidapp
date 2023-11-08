import json
from django.db import models
from rssreader.models import FeedEntry

class Job(models.Model):
    feed = models.OneToOneField(FeedEntry, on_delete=models.CASCADE)
    summary = models.TextField(default='')
    proposal = models.TextField(default='')
    question = models.TextField(default='')
    answers = models.JSONField(null=True, blank=True)
    status = models.CharField(
        max_length=10, 
        choices=[
            ('created', 'Created'),     # job created 
            ('written', 'Written'),     # bid text written
            ('pending', 'pending'),     # bid is in pending
            ('posted', 'Posted'),       # bid posted
            ('failed', 'Failed')        # bid failed (due to bidmaker or auto bidder)
        ],
        default='created'
    )
    dtCreated = models.DateTimeField(auto_now_add=True)
    dtWritten = models.DateTimeField(null=True, blank=True)
    dtPending = models.DateTimeField(null=True, blank=True)
    dtPosted = models.DateTimeField(null=True, blank=True)
    dtFailed = models.DateTimeField(null=True, blank=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"Job for: {self.feed.title}"

    def answerCount(self):
        if self.answers:
            answers = json.load(self.answers)
            return len(answers)
        
    def getAnswers(self):
        if self.answers:
            answers = json.load(self.answers)
            return answers
