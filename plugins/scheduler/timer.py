from threading import Thread, Event
import time


class TimerThread(Thread):
    def __init__(self, event, interval, callback):
        Thread.__init__(self)
        self.stopped = event
        self.interval = interval
        self.callback = callback
        
    def run(self):
        self.callback()
        while not self.stopped.wait(self.interval):
            try:
                self.callback()
            except:
                pass


if __name__ == "__main__":
    
    def callback():
        print ('timer')
        
    stopFlag = Event()
    thread = TimerThread(stopFlag, 1, callback)
    thread.start()
    # this will stop the timer
    time.sleep(10)
    stopFlag.set()