from django.db import models
from django.contrib.auth.models import User


class Benefits(models.Model):
    profile = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='benefit_user')
    time_stamp = models.DateField()
    title = models.CharField(max_length=250, blank=False)
    amount = models.FloatField()
    sender = models.CharField(max_length=250, blank=False)
    
    def __str__(self):
        return self.title