from django.contrib.auth.models import User
from django.db import models


class TelephoneNumber(models.Model):
    owner = models.ForeignKey(User, related_name='user_owner', on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    voters = models.ManyToManyField(User)
