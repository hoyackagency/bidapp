import json
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.db import transaction
from .models import Worker
from .forms import WorkerForm


def worker_list_view(request):
    workers = Worker.objects.all().order_by('wid')

    worker_ids = []
    for worker in workers:
        worker_ids.append(worker.wid)
    
    if request.is_ajax():
        if workers.count() > 0:
            result = []
            for worker in workers:
                result.append({
                    "worker_id": str(worker.id),
                    "wid": str(worker.wid),
                    "name": worker.name,
                    "description": worker.description,
                    "ipaddress": worker.ipaddress,
                    "alive": worker.alive,
                    "running": worker.running,
                    "commands": worker.commands
                })
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        context = {
            "workers"   : workers,
            "view_name" : "WORKERS"
        }
        return render(request, "workers/worker_list.html", context) 


@transaction.atomic
def worker_create_view(request):
    
    if request.method == 'POST':
        form = WorkerForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            new_worker = form.save() 
            return redirect(reverse_lazy('worker_list'))
    else:
        form = WorkerForm()
        
        context = {
            "form"      : form,
            "view_name" : "WORKERS"
        }
    
        return render(request, "workers/worker_create.html", context)


@transaction.atomic
def worker_update_view(request, *args, **kwargs):
    
    if 'pk' not in kwargs:
        return redirect(reverse_lazy('worker_list'))
        
    worker_id = kwargs['pk']
    worker = get_object_or_404(Worker, id=worker_id)
    
    if request.method == 'POST':
        form = WorkerForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('worker_list')) 
    else:
        context = {
            "worker"    : worker,
            "view_name" : 'WORKERS'
        }
        return render(request, 'workers/worker_update.html', context)
    
    
@transaction.atomic
def worker_delete_view(request, *args, **kwargs):
    
    if 'pk' not in kwargs:
        return redirect(reverse_lazy('worker_list'))
        
    worker_id = kwargs['pk']
    worker = get_object_or_404(Worker, id=worker_id)
  
    if request.method == 'POST':
        worker_id = request.POST.get("worker_id")
        worker = get_object_or_404(Worker, id=worker_id)
        worker.delete()
        return redirect(reverse_lazy('worker_list'))
    else:      
        context = {
            "worker"    : worker,
            "view_name" : "WORKERS"
        }
        
        return render(request, "workers/worker_delete.html", context)
