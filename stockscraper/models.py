from django.db import models

# Create your models here.
from django.urls import reverse

class NameObject(models.Model):
    name = models.CharField(max_length=200, help_text='enter some text')

    def __str__(self):
        return self.name

class Counter:
    count = 0

    def increment(self):
        self.count += 1
        return self.count
