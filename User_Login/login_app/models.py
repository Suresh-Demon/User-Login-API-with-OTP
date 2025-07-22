from django.db import models
from django.utils import timezone
# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    is_verifed =models.BooleanField(default=False)


class OTP(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    otp_code = models.CharField(max_length = 6)
    created_at = models.DateTimeField(default=timezone.now)
