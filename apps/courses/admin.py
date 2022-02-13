from django.contrib import admin

from .models import Course, CourseReview, Exercise

# Register your models here.

admin.site.register(Exercise)
admin.site.register(Course)
admin.site.register(CourseReview)
