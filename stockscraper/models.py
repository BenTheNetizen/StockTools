from django.db import models

# Create your models here.
from django.urls import reverse

class Counter:
    count = 0

    def increment(self):
        self.count += 1
        return self.count
