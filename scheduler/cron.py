import requests
import threading
from datetime import datetime
from django.conf import settings

from rssreader.views import parse_rss_feed
from jobs.models import Job


def parse_feeds():
    if settings.DEBUG:
        print("parse rss feed")
    result = parse_rss_feed()
    if settings.DEBUG:
        print("parse rss feed result :", result)


def __make_bid_from_chatgpt(question):
    response = requests.get(settings.BIDMAKER_URL, params={'Summary': question})
    if response.status_code == 200:
        # RFP->question, Summary, Proposal(Proposal:\n\n), Questions
        result = response.json()
        summary = result["Summary"]
        proposal = result["Proposal"]
        questions = result["Questions"]
        return summary, proposal, questions
    else:
        raise Exception(f"Error: {response.status_code}, Failed to make bid of {question}")


def doWriteBids(jobs):
    for job in jobs:
        feed = job.feed
        if settings.DEBUG:
            print ("writting bid for :", feed.title)
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
            # job.status = "failed"
            # job.dtFailed = datetime.now().isoformat()
            # job.save()
            continue


def write_bids():
    if settings.DEBUG:
        print("writting bids...")

    jobs = Job.objects.filter(status='created')
    counts = jobs.count()
    if counts > 0:
        writeThread = threading.Thread(target=doWriteBids, args=(jobs,))
        writeThread.start()
    else:
        if settings.DEBUG:
            print("no bids to write!")
    

def do_schedule():
    # parse rss feed
    parse_feeds()

    # check the jobs to make bid
    write_bids()
