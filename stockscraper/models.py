from django.db import models

# Create your models here.
from django.urls import reverse
import uuid #Required for unique book instances

#Counter model is used to numerate the entries in the table returned in the StockScraper tool
class Counter:
    count = 0

    def increment(self):
        self.count += 1
        return self.count

#model for blogposts
class Blog(models.Model):
    title = models.CharField(max_length=200)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the blog post')

    date = models.DateField()

    post = models.TextField(max_length=4000)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

#model for visitor count and search count
class VisitorCount(models.Model):
    visitor_count = models.IntegerField()

    search_count = models.IntegerField()

    def increment_visitors(self):
        self.visitor_count += 1
        return self.visitor_count

    def increment_searches(self):
        self.search_count += 1
        return self.search_count
