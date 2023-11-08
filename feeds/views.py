import json
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.urls import reverse_lazy
from .models import FeedEntry, Job


def feed_list_view(request):
    feeds = FeedEntry.objects.filter(archived=False).order_by('id')

    if request.is_ajax():
        result = []
        feeds = FeedEntry.objects.filter(archived=False).order_by('-id')

        if feeds.count() > 0:
            for feed in feeds:
                result.append({
                    "id"        : feed.id,
                    "title"     : feed.title,
                    "link"      : feed.link,
                    "content"   : feed.content,
                    "pay_range" : feed.pay_range,
                    "job_type"  : feed.job_type,
                    "category"  : feed.category,
                    "skills"    : feed.skills,
                    "country"   : feed.country,
                    "published_date": feed.published_date.isoformat()
                })
        return HttpResponse(json.dumps(result), content_type='application/json')

    context = {}
    context["is_staff"] = False
    context["view_name"] = "FEEDS"
    context["feeds"] = feeds
        
    return render(request, "feeds/feed_list.html", context) 


def feed_detail_view(request, *args, **kwargs):
    try:
        if 'feed_id' not in kwargs:
            return redirect(reverse_lazy('feed_list'))
        
        feed_id = kwargs['feed_id']
        feed = FeedEntry.objects.get(id=feed_id)
        
        needRedirect = False
        if request.method == "GET":
            status = request.GET.get("status")
            if status == "decline":
                feed.archived = True
                feed.save()
                feed = None
                needRedirect = True
            elif status == "accept":
                try:
                    job = Job.objects.get(feed=feed)
                except Job.DoesNotExist:
                    job = Job.objects.create(feed=feed)
                feed.archived = True
                feed.save()
                feed = None
                needRedirect = True
            elif status == "prev":
                feed = FeedEntry.objects.filter(
                    id__lt=feed.id,
                    archived=False
                ).order_by('id').first()
                needRedirect = True
            elif status == "next":
                feed = FeedEntry.objects.filter(
                    id__gt=feed.id,
                    archived=False
                ).order_by('id').first()
                needRedirect = True

            if not feed:
                feed = FeedEntry.objects.filter(
                    archived=False
                ).order_by('id').first()

        if not feed:
            return redirect(reverse_lazy('feed_list'))
        else:
            if needRedirect:
                return redirect(reverse_lazy('feed_detail', kwargs={'feed_id': feed.id}))
            else:
                return render(request, "feeds/feed_detail.html", {"feed": feed})
    except FeedEntry.DoesNotExist:
        return redirect(reverse_lazy('feed_list'))
