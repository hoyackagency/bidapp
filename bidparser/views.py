from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job, FeedEntry
from .serializers import JobSerializer
from rssreader.serializers import FeedEntrySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

class FeedEntryView(APIView):

    def get(self, request):
        recycle = request.query_params.get('recycle', None)
        feed_entry_id = request.query_params.get('feed_entry_id', None)

        feed_entry = None

        if recycle and feed_entry_id:
            try:
                current_entry = FeedEntry.objects.get(id=feed_entry_id)
                feed_entry = FeedEntry.objects.filter(
                    id__gt=current_entry.id,
                    archived=False
                ).exclude(
                    job__status__in=['accept', 'decline']
                ).order_by('id').first()
            except FeedEntry.DoesNotExist:
                return Response({'error': 'Feed entry with given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if not feed_entry:
            feed_entry = FeedEntry.objects.filter(
                archived=False
            ).exclude(
                job__status__in=['accept', 'decline']
            ).order_by('id').first()

        if not feed_entry:
            blank_data = {
                "id": 0,
                "feed": {"feed_name": ""},
                "title": "",
                "link": "",
                "published_date": "",
                "content": "",
                "pay_range": "",
                "job_type": "",
                "category": "",
                "skills": "",
                "country": "",
                "archived": True
            }
            return Response(blank_data)

        try:
            job = Job.objects.get(feed_entry=feed_entry)
            serializer = JobSerializer(job)
            return Response(serializer.data)
        except Job.DoesNotExist:
            serializer = FeedEntrySerializer(feed_entry)
            return Response(serializer.data)
        
    def post(self, request):
        feed_entry_id = request.data.get('feed_entry_id')
        job_status = request.data.get('status')

        if not feed_entry_id or not job_status:
            return Response({'error': 'Both feed_entry_id and status are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if job_status not in ('accept', 'decline', 'recycle'):
            return Response({'error': 'Invalid status value. It must be either "accept", "decline", or "recycle".'}, status=status.HTTP_400_BAD_REQUEST)

        feed_entry = get_object_or_404(FeedEntry, id=feed_entry_id)

        if job_status == 'decline':
            feed_entry.archived = True
            feed_entry.save()
            return Response({'message': f'FeedEntry {feed_entry_id} archived.'})
        else:
            if Job.objects.filter(feed_entry=feed_entry).exists():
                return Response({'error': 'Job already exists for the given feed_entry.'}, status=status.HTTP_400_BAD_REQUEST)

            Job.objects.create(feed_entry=feed_entry, status=job_status)
            return Response({'message': 'Job created successfully.'})
