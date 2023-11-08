import feedparser
import pytz
import re
import traceback
from datetime import datetime
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets

from .models import FeedEntry, RSSFeed
from .serializers import FeedEntrySerializer, RSSFeedSerializer
from .utils import clean_text, parse_content


class FeedEntryViewSet(viewsets.ModelViewSet):
    queryset = FeedEntry.objects.all()
    serializer_class = FeedEntrySerializer


class RSSFeedViewSet(viewsets.ModelViewSet):
    queryset = RSSFeed.objects.all()
    serializer_class = RSSFeedSerializer


def parse_rss_feed_view(request):
    try:
        result = parse_rss_feed()
        return JsonResponse(result)
    except Exception as e:
        message = f"Error parsing RSS feed: {str(e)}"
        data = {'message': message}
        traceback.print_exc()  # Print the traceback for detailed error information
        return JsonResponse(data)


def parse_rss_feed():
    created_count = 0
    skipped_count = 0

    rss_feeds = RSSFeed.objects.all()
    for rss_feed in rss_feeds:
        if rss_feed.enabled:
            url = rss_feed.url
            feed_name = rss_feed.feed_name

            feed_entries = feedparser.parse(url)
            for entry in feed_entries.entries:
                try:
                    # Remove the suffix ' - Upwork' from the title
                    suffix = ' - Upwork'
                    if entry.title.endswith(suffix):
                        title = entry.title[:-len(suffix)]
                    else:
                        title = entry.title

                    link = entry.get('link', '')  # Provide a default value if link is not present
                    published_date_str = entry.get('published', '')
                    published_date = parse_datetime(published_date_str) if published_date_str else None

                    if not published_date:
                        # Parse the date manually
                        published_date = datetime.strptime(published_date_str, '%a, %d %b %Y %H:%M:%S %z').astimezone(pytz.UTC)

                    original_content = entry.content[0].value if entry.content else ''
                    content = clean_text(original_content)

                    if 'Hourly Range' in content:
                        content = content.split('Hourly Range', 1)[0]
                    elif 'Budget' in content:
                        content = content.split('Budget', 1)[0]
                    elif 'Posted On' in content:
                        content = content.split('Posted On', 1)[0]
                    
                    content = re.sub('<br /><br /><b>$', '', content)

                    # Check if a similar entry already exists
                    existing_entry = FeedEntry.objects.filter(title=title, link=link, feed=rss_feed).first()
                    if existing_entry:
                        skipped_count += 1
                        continue

                    job_title, pay_range, job_type, category, skills, country = parse_content(original_content)

                    feed_entry = FeedEntry.objects.create(
                        title=title,
                        link=link,
                        published_date=published_date,
                        content=content,  # This is the stripped and cleaned content
                        pay_range=pay_range,
                        job_type=job_type,
                        category=category,
                        skills=skills,
                        country=country,
                        feed=rss_feed
                    )
                    feed_entry.save()
                    created_count += 1
                except Exception as e:
                    print(f"Error parsing entry: {entry.title}")
                    print(e)
                    traceback.print_exc()  # Print the traceback for detailed error information

    message = f"RSS feed parsing completed successfully. Created: {created_count}, Skipped: {skipped_count}"
    return {'message': message}

