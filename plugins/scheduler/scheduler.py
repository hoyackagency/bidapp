from threading import Event
from django.conf import settings
from .timer import TimerThread


SCHEDULE_PERIOD = 60    # 1 min


def __task_schedule():
    if settings.DEBUG:
        print ("scheduler called")


def run_task_scheduler():
    stopFlag = Event()

    thread = TimerThread(stopFlag, SCHEDULE_PERIOD, __task_schedule)
    thread.start()
    
    thread.join()
    print ("scheduler finished")    
