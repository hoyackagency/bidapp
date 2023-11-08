import json
import requests
import threading
from datetime import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect

from rssreader.views import parse_rss_feed_view
from jobs.models import Job


def __make_bid_from_chatgpt(question):
    response = requests.get(settings.BIDMAKER_URL, params={'Summary': question})
    if response.status_code == 200:
        # RFP->question, Summary, Proposal(Proposal:\n\n), Questions
        result = response.json()
        summary = result["Summary"]
        proposal = result["Proposal"]
        proposal = proposal[11:]
        questions = result["Questions"]
        return summary, proposal, questions
    else:
        raise Exception(f"Error: {response.status_code}, Failed to make bid of {question}")


def doWriteBids(jobs):
    for job in jobs:
        feed = job.feed
        if not feed.content:
            job.status = "failed"
            job.dtFailed = datetime.now().isoformat()
            job.save()
            continue

        try:
            summary, proposal, questions = __make_bid_from_chatgpt(feed.content)
            job.summary = summary
            job.proposal = proposal
            job.question = questions
            job.dtWritten = datetime.now().isoformat()
            job.status = "written"
            job.save() 
        except:
            job.status = "failed"
            job.dtFailed = datetime.now().isoformat()
            job.save()


def write_bids():
    if settings.DEBUG:
        print("writting bids...")

    jobs = Job.objects.filter(status='created')
    counts = jobs.count()
    if counts > 0:
        doWriteBids(jobs)
    

def do_schedule(request):
    # parse rss feed
    parse_rss_feed_view(request)
    
    # check the jobs to make bid
    write_bids()

    return HttpResponse({"message": "done schedule"})
