from django.contrib import admin

# Register your models here.
from .models import Job
from .models import Bid
from .models import Prompt

admin.site.register(Job)
admin.site.register(Bid)
admin.site.register(Prompt)