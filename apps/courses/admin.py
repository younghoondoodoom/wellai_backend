from django.contrib import admin

from .models import Course, Exercise

# Register your models here.

admin.site.register(Exercise)
admin.site.register(Course)
