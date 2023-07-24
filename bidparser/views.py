from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job, FeedEntry
from .serializers import JobSerializer
from rssreader.serializers import FeedEntrySerializer
from .handlers import get_next_feed_entry, create_or_update_job
from .serializers import JobSerializer
from django.db.models import Prefetch
from rest_framework import generics
from rest_framework import viewsets

class FeedEntryView(APIView):

    def get(self, request):
        recycle = request.query_params.get('recycle', None)
        feed_entry_id = request.query_params.get('feed_entry_id', None)

        feed_entry, error, status_code = get_next_feed_entry(recycle, feed_entry_id)
        if status_code == 404:
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        elif status_code == 200 and error:
            return Response(error)

        try:
            job = Job.objects.get(feed_entry=feed_entry)
            serializer = JobSerializer(job)
        except Job.DoesNotExist:
            serializer = FeedEntrySerializer(feed_entry)

        return Response(serializer.data)

    def post(self, request):
        feed_entry_id = request.data.get('feed_entry_id')
        job_status = request.data.get('status')

        response, status_code = create_or_update_job(feed_entry_id, job_status)
        return Response(response, status=status_code)

class JobsView(generics.ListAPIView):
    queryset = Job.objects.all().prefetch_related(
        Prefetch('feed_entry', queryset=FeedEntry.objects.all())
    )
    serializer_class = JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing jobs.
    """
    queryset = Job.objects.all().prefetch_related(
        Prefetch('feed_entry', queryset=FeedEntry.objects.all())
    )
    serializer_class = JobSerializer