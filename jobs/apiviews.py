from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from rssreader.serializers import FeedEntrySerializer
from .models import FeedEntry, Job
from .serializers import JobSerializer


def get_next_feed_entry(recycle, feed_entry_id):
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
            return None, {'error': 'Feed entry with given id does not exist.'}, 404

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
        return None, blank_data, 200

    return feed_entry, None, None


def create_or_update_job(feed_entry_id, job_status):
    if not feed_entry_id or not job_status:
        return {'error': 'Both feed_entry_id and status are required.'}, 400

    if job_status not in ('accept', 'decline', 'recycle'):
        return {'error': 'Invalid status value. It must be either "accept", "decline", or "recycle".'}, 400

    feed_entry = get_object_or_404(FeedEntry, id=feed_entry_id)

    if job_status == 'decline':
        feed_entry.archived = True
        feed_entry.save()
        return {'message': f'FeedEntry {feed_entry_id} archived.'}, 200
    elif job_status == 'accept':
        try:
            job = Job.objects.get(feed_entry=feed_entry)
            return {'error': 'Job already exists for the given feed_entry.'}, 400
        except Job.DoesNotExist:
            job = Job.objects.create(feed_entry=feed_entry, status=job_status)
            Bid.objects.create(job=job)
            return {'message': 'Job created successfully.'}, 200
    else:
        return {'message': f'Unknown job status : {job_status}'}, 400


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