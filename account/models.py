from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    referral_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# class Referrals(models.Model):
#     user_id = models.OneToOneField(User, on_delete=models.CASCADE)
#     ref_id = models.OneToOneField(User, on_delete=models.CASCADE)
