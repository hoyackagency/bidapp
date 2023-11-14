import json
from datetime import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.urls import reverse_lazy

from plugins.rabbitmq.publish import RabbitMQPublisher
from .models import FeedEntry, Job


MODULE_ID_UPWORKBID = 1

def job_list_view(request):
    jobs = Job.objects.filter(archived=False).order_by('id')

    if request.is_ajax():
        result = []
        status = request.GET['status']
        job_status = None
        if status == "1":
            job_status = 'created'
        elif status == "2":
            job_status = 'written'
        elif status == "3":
            job_status = 'pending'
        elif status == "4":
            job_status = 'posted'
        elif status == "5":
            job_status = 'failed'

        if job_status:
            jobs = Job.objects.filter(status=job_status, archived=False).order_by('-id')
        else:
            jobs = Job.objects.filter(archived=False).order_by('-id')

        if jobs.count() > 0:
            for job in jobs:
                result.append({
                    "id"        : job.id,
                    "title"     : job.feed.title,
                    "link"      : job.feed.link,
                    "content"   : job.feed.content,
                    "pay_range" : job.feed.pay_range,
                    "job_type"  : job.feed.job_type,
                    "category"  : job.feed.category,
                    "skills"    : job.feed.skills,
                    "country"   : job.feed.country,
                    "published_date": job.feed.published_date.isoformat(),
                    "status"    : job.status,
                })
        return HttpResponse(json.dumps(result), content_type='application/json')

    context = {}
    context["is_staff"] = False
    context["view_name"] = "JOBS"
    context["jobs"] = jobs
        
    return render(request, "jobs/job_list.html", context) 


def publishJob(job):
    if settings.DEBUG:
        print(f"Job publish commands : {job.feed.title}")

    # post the run to the message queue api
    rabbitmqPublisher = RabbitMQPublisher()
    command_at = datetime.utcnow().timestamp()
    run_command = {
        "command": "run",
        "workers": [1],
        "parameters": {
            "module_id"     : MODULE_ID_UPWORKBID,
            "bid": {
                "id"            : job.id,
                "url"           : job.feed.link,
                "title"         : job.feed.title,
                "hourly"        : True if job.feed.job_type == "Hourly" else False,
                "summary"       : job.summary,
                "proposal"      : job.proposal,
                "question"      : job.question,
                "command_at"    : command_at
            }
        }
    }
    rabbitmqPublisher.publish_run_command(run_command)
        

def job_detail_view(request, *args, **kwargs):
    try:
        if 'job_id' not in kwargs:
            return redirect(reverse_lazy('job_list'))
        
        job_id = kwargs['job_id']
        job = Job.objects.get(id=job_id)
        
        needRedirect = False
        if request.method == "GET":
            action = request.GET.get("action")
            if action == "archive":
                job.archived = True
                job.save()
                job = None
                needRedirect = True
            elif action == "prev":
                job = Job.objects.filter(
                    id__lt=job_id,
                    archived=False,
                    status__in=["created", "written"]
                ).order_by('-id').first()
                needRedirect = True
            elif action == "next":
                job = Job.objects.filter(
                    id__gt=job_id,
                    archived=False,
                    status__in=["created", "written"]
                ).order_by('id').first()
                needRedirect = True

            if not job:
                job = Job.objects.filter(
                    archived=False,
                    status__in=["created", "written"]
                ).order_by('-id').first()

        elif request.method == "POST":
            submitType = request.POST.get("submitType")
            summary = request.POST.get("summary")
            proposal = request.POST.get("proposal")
            question = request.POST.get("question")

            job.summary = summary
            job.proposal = proposal
            job.question = question
            job.save()

            if submitType == "Post":
                publishJob(job)

                job.status = "pending"
                job.save()
                
                job = Job.objects.filter(
                    id__gt=job_id,
                    archived=False,
                    status__in=["created", "written", "failed"]
                ).order_by('id').first()
                needRedirect = True
                if not job:
                    job = Job.objects.filter(
                        archived=False,
                        status__in=["created", "written", "failed"]
                    ).order_by('-id').first()

        if not job:
            return redirect(reverse_lazy('job_list'))
        else:
            if needRedirect:
                return redirect(reverse_lazy('job_detail', kwargs={'job_id': job.id}))
            else:
                return render(request, "jobs/job_detail.html", {"job": job})
    except FeedEntry.DoesNotExist:
        return redirect(reverse_lazy('job_list'))


def job_archive_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    job.archived = True
    job.save()

    return redirect(reverse_lazy('job_list'))
