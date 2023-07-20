from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job, FeedEntry
from .serializers import JobSerializer


class FeedEntryView(APIView):
    def get(self, request):
        # Fetch the first FeedEntry that is not related to a Job 
        # or is related to a Job with a 'recycle' status
        feed_entry = FeedEntry.objects.filter(
            # exclude feed entries that are related to a job and 
            # the job's status is not 'recycle'
            ~models.Q(job__status__in=['accept', 'decline'])
        ).order_by('id').first()  # Sorts the feed entries and gets the first

        if not feed_entry:
            return Response({'message': 'No feed entry found.'})

        # If a related job exists, serialize it, else return the feed entry details
        try:
            job = Job.objects.get(feed_entry=feed_entry)
            serializer = JobSerializer(job)
            return Response(serializer.data)
        except Job.DoesNotExist:
            return Response({'title': feed_entry.title, 'link': feed_entry.link})

