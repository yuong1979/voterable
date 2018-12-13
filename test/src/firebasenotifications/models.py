from django.db import models

# Create your models here.


class DeviceToken(models.Model):

    user_id = models.IntegerField()
    device_token = models.CharField(max_length=300, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
