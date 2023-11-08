# myproject/webapp/views.py

import requests
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    response = requests.get(f'{settings.BIDAPP_URL}/view')
    data = response.json()
#    return render(request, 'webapp/index.html', {'data': data})
    if data.get('id') == 0:
        # if id is 0, render a different template
        return render(request, 'webapp/end_of_list.html')
    else:
        return render(request, 'webapp/index.html', {'data': data})

@csrf_exempt
def thumbs_updown(request):
    if request.method == 'POST':
        feed_entry_id = request.POST.get('id')
        status = request.POST.get('status')
        response = requests.post(f'{settings.BIDAPP_URL}/view/', data={'feed_entry_id': feed_entry_id, 'status': status})
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=400)