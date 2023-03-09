from django.urls import path

from .views import LessonView

urlpatterns = [
    path("<int:id>-<slug:slug>/", LessonView.as_view(), name="lesson"),
]
