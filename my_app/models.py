from django.db import models


# Create your models here.


class ChargePoint(models.Model):
    STATUS_READY = 1
    STATUS_CHARGING = 2
    STATUS_WAITING = 3
    STATUS_ERROR = 4
    STATUS_CHOICES = (
        (STATUS_READY, 'Ready'),
        (STATUS_CHARGING, 'Charging'),
        (STATUS_WAITING, 'Waiting'),
        (STATUS_ERROR, 'Error')
    )
    name = models.CharField(max_length=32, unique=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_READY)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
