from __future__ import unicode_literals

from django.db import models
from redditusers.models import reddituser

# Create your models here.
class redditcomment(models.Model):
    user = models.ForeignKey(
     reddituser,
     on_delete=models.CASCADE,
    )



    # def __str__(self):
    #     return format(self.user.username)