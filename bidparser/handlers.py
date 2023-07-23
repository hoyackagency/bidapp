# handlers.py

from .models import Job, FeedEntry
from django.shortcuts import get_object_or_404

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
    else:
        if Job.objects.filter(feed_entry=feed_entry).exists():
            return {'error': 'Job already exists for the given feed_entry.'}, 400

        Job.objects.create(feed_entry=feed_entry, status=job_status)
        return {'message': 'Job created successfully.'}, 200
