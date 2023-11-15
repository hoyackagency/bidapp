from datetime import datetime, timezone
from django.shortcuts import render

from feeds.models import FeedEntry
from .models import Settings


def __getPrice(pay_range):
    price = None
    value = pay_range.replace('$', '').replace(',', '')
    try:
        if '-' in value:
            ratings = value.split('-')
            for rating in ratings:
                rating = int(float(rating))
                if not price:
                    price = rating
                else:
                    if rating > price:
                        price = rating
        else:
            price = int(float(value))
    except:
        pass
    
    return price

  
def settings(request):
    if Settings.objects.count() == 0:
        settings = Settings.objects.create()
        settings.save()
        
    settings = Settings.objects.first()        
    
    if request.method == 'POST':
        fixedMinPrice = request.POST.get("fixedMinPrice")
        hourlyMinRate = request.POST.get("hourlyMinRate")
        archiveDays = request.POST.get("archiveDays")
        settings.fixedMinPrice = int(fixedMinPrice)
        settings.hourlyMinRate = int(hourlyMinRate)
        settings.archiveDays = int(archiveDays)
        settings.save()

        now = datetime.now(timezone.utc)
        feeds = FeedEntry.objects.filter(archived=False).order_by('-id')
        for feed in feeds:
            try:
                if feed.job_type == "Fixed":
                    if settings.fixedMinPrice > 0:
                        price = __getPrice(feed.pay_range)
                        if price and price < settings.fixedMinPrice:
                            feed.archived = True
                            feed.save()
                            continue

                elif feed.job_type == "Hourly":
                    if settings.hourlyMinRate > 0:
                        price = __getPrice(feed.pay_range)
                        if price and price < settings.hourlyMinRate:
                            feed.archived = True
                            feed.save()
                            continue

                if settings.archiveDays > 0:
                    dtDiff = now - feed.published_date
                    if dtDiff.days >= settings.archiveDays:
                        feed.archived = True
                        feed.save()
            except Exception as e:
                continue
        
    return render(request, 'settings/settings.html', {
        'view_name' : 'SETTINGS',
        'settings'  : settings
    })
