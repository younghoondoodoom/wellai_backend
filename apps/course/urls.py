from django.urls import path, include
from .views import ExerciseList, ExerciseCourseList

urlpatterns = [
    # test api
    path('exerciselist', ExerciseList.as_view() ,name="exercise-list"),
    path('courselist', ExerciseCourseList.as_view() ,name="course-list")
]