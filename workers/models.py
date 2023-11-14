from django.db import models
from datetime import datetime

# Create your models here.

class Worker(models.Model):
    
    # worker id
    wid = models.IntegerField(
        default=-1
    )
    
    # name
    name = models.CharField(
        max_length=32,
        null=False
    )
    
    # description
    description = models.CharField(
        max_length=256,
        null=False
    )
    
    # ip address
    ipaddress = models.CharField(
        max_length=32,
        blank=True
    )
    
    # is alive
    alive = models.BooleanField(
        default=False
    )
    
    # is running
    running = models.BooleanField(
        default=False
    )
    
    # count of the remained commands
    commands = models.IntegerField(
        default=0
    )
    
    # started timestamp
    started_at = models.IntegerField(
        default=0
    )
    
    # updated timestamp
    updated_at = models.IntegerField(
        default=0
    )
    
    def __str__(self):
        return self.name
    
    def set_status(self, ipaddress, running, commands, started_at):
        self.alive = True
        self.ipaddress = ipaddress
        self.running = running
        self.commands = commands
        self.started_at = started_at
        self.updated_at = int(datetime.utcnow().timestamp())
        self.save()
        
    def check_alive(self):
        now_ts = int(datetime.utcnow().timestamp())
        if now_ts - self.updated_at > 300:      # 5mins
            self.ipaddress = "" 
            self.alive = False
            self.running = False
            self.commands = 0
            self.save()
    
    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"
        