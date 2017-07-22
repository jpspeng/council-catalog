from __future__ import unicode_literals

from datetime import datetime
# Create your models here.
#from django.contrib.auth.models import User


from django.db import models

import os

from django.conf import settings

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    file_upload = models.FileField(upload_to = '')

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)

    