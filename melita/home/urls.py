from django.urls import path, re_path

from .views import LessonListPartialView, LessonListView, LessonView

urlpatterns = [
    path("lessons/<int:id>-<slug:slug>/", LessonView.as_view(), name="lesson"),
    path("lessons/filter-list", LessonListPartialView.as_view(), name="lesson_list_partial"),
    re_path(r"^$", LessonListView.as_view(), name="lesson_list"),
]
