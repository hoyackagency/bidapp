from django.db import models

class Settings(models.Model):

    # fixedjob min price
    fixedMinPrice = models.IntegerField(
        default=0
    )

    # hourlyjob min rate
    hourlyMinRate = models.IntegerField(
        default=0
    )

    # auto archive after days
    archiveDays = models.IntegerField(
        default=0
    )

    # connects (read only)
    connects = models.IntegerField(
        default=0
    )