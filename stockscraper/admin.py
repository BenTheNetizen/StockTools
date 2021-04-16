from django.contrib import admin

# Register your models here.
from .models import Blog, VisitorCount

admin.site.register(Blog)
admin.site.register(VisitorCount)
