import feedparser
from django.utils.dateparse import parse_datetime
from .models import FeedEntry, RSSFeed
import traceback
from datetime import datetime
import pytz
from .utils import parse_content
from django.http import JsonResponse
import re

def parse_rss_feed(request):
    try:
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
                        content = original_content
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
                            content=content,  # This is the stripped content
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
        data = {'message': message}
        return JsonResponse(data)
    except Exception as e:
        message = f"Error parsing RSS feed: {str(e)}"
        data = {'message': message}
        traceback.print_exc()  # Print the traceback for detailed error information
        return JsonResponse(data)


