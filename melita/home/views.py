from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from .models import Lesson


class LessonView(TemplateView):
    template_name = "home/lesson_view.html"

    def get_context_data(self, id, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lesson"] = get_object_or_404(Lesson, id=id)
        return context
