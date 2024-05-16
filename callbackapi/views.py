import json
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from jobs.models import Job
from settings.models import Settings
from workers.models import Worker


# host status
HOST_STATUS_RUNNING         = 200
HOST_STATUS_IDLE            = 201

# data error code
SUCCESS                     = 200
SUCCESS_CONNECTS            = 201
ERR_BAD_REQUEST             = 400
ERR_NOT_FOUND               = 404
ERR_NET_TIMEOUT             = 408
ERR_STOPPED                 = 440
ERR_BANNED                  = 441
ERR_SIGN_IN                 = 442
ERR_JOB_POST                = 443
ERR_JOB_NOT_AVAILABLE       = 444
ERR_GET_CONNECTS            = 445
ERR_NEED_CONNECTS           = 446
ERR_UNKNOWN                 = 449


@csrf_exempt
@require_POST
@transaction.atomic
def worker_callback(request): 
    # get worker callback parameters
    try:
        post_params = json.loads(request.body.decode('utf-8'))

        worker_id = post_params['worker_id']
        ip_address = post_params['ip_addr']
        started_at = post_params['started_at']
        running_status = post_params['running_status']
        remain_commands = post_params['remain_commands']

    except Exception as e:
        return JsonResponse({
            "error": True,
            "message": f"Invalid callback parameters : {str(e)}"
        })
    
    # process worker callback
    try:
        worker = Worker.objects.get(wid=worker_id)

        running = False
        if running_status == HOST_STATUS_RUNNING:
            running = True
        started_at = int(started_at)

        worker.set_status(ip_address, running, remain_commands, started_at)

        return JsonResponse({
            "error": False,
            "message": "Success"
        })
    
    except Worker.DoesNotExist: 
        return JsonResponse({
            "error": True,
            "message": f"Invalid callback parameters : non-exist worker {worker_id}"
        })
    except Exception as e:
        return JsonResponse({
            "error": True,
            "message": f"Callback error : {str(e)}"
        })


@csrf_exempt
@require_POST
@transaction.atomic
def bid_result_callback(request, *args, **kwargs): 
    # get worker callback parameters
    try:
        post_params = json.loads(request.body.decode('utf-8'))

        result = post_params['result']
        module_id = result['data']['module_id']
        job_id = result['data']['id']

        print (f"===>>> bid result : {result}")

        if module_id == settings.MODULE_ID_UPWORKBID:
            job = Job.objects.get(id=job_id)
            if result['error']:
                job.status = "failed"
                if result['code'] == ERR_JOB_NOT_AVAILABLE:
                    job.archived = True
                job.save()
            else:
                if result['code'] == SUCCESS:
                    job.status = "posted"
                    job.archived = True
                    job.save()
                elif result['code'] == SUCCESS_CONNECTS:
                    appSettings = Settings.objects.first()
                    appSettings.connects = result['data']['connects']
                    appSettings.save()

            return JsonResponse({
                "error": False,
                "message": f"Job result callback success : {job_id}"
            })

    except Job.DoesNotExist:
        return JsonResponse({
            "error": True,
            "message": f"Job doesn't exist : {job_id}"
        })
    except Exception as e:
        return JsonResponse({
            "error": True,
            "message": f"Invalid callback parameters : {str(e)}"
        })
