from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from django.utils import translation
from django.views.generic.base import TemplateView

from .models import InstructionMethod, Lesson, LessonTag, Material, PrepTime, Theme


class LessonView(TemplateView):
    template_name = "home/lesson_view.html"

    def get_context_data(self, id, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lesson"] = get_object_or_404(Lesson, id=id)
        return context


def map_attr(objects, key):
    return list(map(lambda o: getattr(o, key), objects))


class LessonListPartialView(TemplateView):
    template_name = "home/lesson_list_partial_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["filters"] = [
            {
                "key": "theme",
                "name": "Theme",
                "icons": [
                    static("icons/filters/themes.svg"),
                    static("icons/filters/themes-hover.svg"),
                ],
                "options": map_attr(Theme.objects.all(), "name"),
            },
            {
                "key": "instruction_method",
                "name": "Main method of instruction",
                "icons": [
                    static("icons/filters/methods.svg"),
                    static("icons/filters/methods-hover.svg"),
                ],
                "options": map_attr(InstructionMethod.objects.all(), "name"),
            },
            {
                "key": "prep_time",
                "name": "Prep time for teacher",
                "icons": [
                    static("icons/filters/prep.svg"),
                    static("icons/filters/prep-hover.svg"),
                ],
                "options": PrepTime.values,
            },
            {
                "key": "materials",
                "name": "Materials",
                "icons": [
                    static("icons/filters/materials.svg"),
                    static("icons/filters/materials-hover.svg"),
                ],
                "options": map_attr(Material.objects.all(), "name"),
            },
            {
                "key": "keywords",
                "name": "Keywords",
                "icons": [
                    static("icons/filters/keywords.svg"),
                    static("icons/filters/keywords-hover.svg"),
                ],
                "options": map_attr(Lesson.keywords.all(), "name"),
            },
        ]

        lessons = Lesson.objects.all()

        for filter_dict in context["filters"]:
            key = filter_dict["key"]
            valid_options = list(map(lambda o: str(o), filter_dict["options"]))
            param_key = f"filter[{key}]"
            param_value = self.request.GET.get(param_key, "")
            param_values = map(str.strip, param_value.split(","))
            params = list(filter(lambda o: o in valid_options, param_values))

            filter_dict["enabled_options"] = params

            if len(params):
                if key == "prep_time":
                    lessons = lessons.filter(prep_time__in=params)
                else:
                    q = {f"{key}__name__in": params}
                    lessons = lessons.filter(**q)

        context["lessons"] = lessons.distinct()

        return context


class LessonListView(LessonListPartialView):
    template_name = "home/lesson_list_view.html"

    def get(self, request, *args, **kwargs):
        new_language = None
        if lang := self.request.GET.get('lang'):
            new_language = lang
            translation.activate(new_language)

        response = super().get(request, *args, **kwargs)

        if new_language:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, new_language)

        return response
