from django.contrib import admin

from .models import BookMark, Course, CourseReview, Exercise, Tag

admin.site.register(Exercise)
admin.site.register(Course)
admin.site.register(CourseReview)
admin.site.register(Tag)
admin.site.register(BookMark)
