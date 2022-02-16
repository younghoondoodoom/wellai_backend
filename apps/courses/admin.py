from django.contrib import admin

from .models import Course, CourseReview, Exercise, Tag

# Register your models here.

admin.site.register(Exercise)
admin.site.register(Course)
admin.site.register(CourseReview)
admin.site.register(Tag)
