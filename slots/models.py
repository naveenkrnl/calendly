from django.db import models
from accounts.models import UserProfile

# Create your models here.

class UserSlots(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT,related_name='user_profile')
    slot_booked_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reason = models.CharField(max_length=200)
