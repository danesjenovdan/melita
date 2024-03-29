from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from icu import Collator, Locale

from .models import Duration, Lesson, Material, PrepTime, StudentLevel, Theme

VALID_LANG_IDS = [lang[0] for lang in settings.LANGUAGES]


class LessonView(TemplateView):
    template_name = "home/lesson_view.html"

    def get(self, request, *args, **kwargs):
        lesson = get_object_or_404(Lesson, id=kwargs["id"])
        translation.activate(lesson.language.code)
        return super().get(request, *args, **kwargs)

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

        lang = translation.get_language()
        collator = Collator.createInstance(Locale(lang))
        name_attr = "name" if lang == "en" else f"name_{lang}"

        lessons = Lesson.objects.all().filter(language__code=lang)

        keywords = list(lessons.values_list("keywords__name", flat=True).distinct())
        keywords = filter(lambda o: bool(o), keywords)
        sorted_keywords = sorted(set(keywords), key=lambda o: collator.getSortKey(o))

        context["filters"] = [
            {
                "key": "theme",
                "name": "Theme",
                "translated_name": _("Theme"),
                "icons": [
                    static("icons/filters/themes.svg"),
                    static("icons/filters/themes-hover.svg"),
                ],
                "options": map_attr(
                    Theme.objects.exclude(**{f"{name_attr}": ""}), name_attr
                ),
            },
            # {
            #     "key": "instruction_method",
            #     "name": "Main method of instruction",
            #     "translated_name": _("Main method of instruction"),
            #     "icons": [
            #         static("icons/filters/methods.svg"),
            #         static("icons/filters/methods-hover.svg"),
            #     ],
            #     "options": map_attr(
            #         InstructionMethod.objects.exclude(**{f"{name_attr}": ""}), name_attr
            #     ),
            # },
            {
                "key": "duration",
                "name": "Duration",
                "translated_name": _("Duration"),
                "icons": [
                    static("icons/filters/methods.svg"),
                    static("icons/filters/methods-hover.svg"),
                ],
                "options": map_attr(
                    Duration.objects.exclude(**{f"{name_attr}": ""}), name_attr
                ),
            },
            {
                "key": "student_level",
                "name": "Level",
                "translated_name": _("Level"),
                "icons": [
                    static("icons/filters/student-level.svg"),
                    static("icons/filters/student-level-hover.svg"),
                ],
                "options": map_attr(
                    StudentLevel.objects.exclude(**{f"{name_attr}": ""}), name_attr
                ),
            },
            {
                "key": "prep_time",
                "name": "Prep time for teacher",
                "translated_name": _("Prep time for teacher"),
                "icons": [
                    static("icons/filters/prep.svg"),
                    static("icons/filters/prep-hover.svg"),
                ],
                "options": PrepTime.values,
            },
            {
                "key": "materials",
                "name": "Materials",
                "translated_name": _("Materials"),
                "icons": [
                    static("icons/filters/materials.svg"),
                    static("icons/filters/materials-hover.svg"),
                ],
                "options": map_attr(
                    Material.objects.exclude(**{f"{name_attr}": ""}), name_attr
                ),
            },
            {
                "key": "keywords",
                "name": "Keywords",
                "translated_name": _("Keywords"),
                "icons": [
                    static("icons/filters/keywords.svg"),
                    static("icons/filters/keywords-hover.svg"),
                ],
                "options": list(sorted_keywords),
            },
        ]

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
                elif key == "keywords":
                    lessons = lessons.filter(keywords__name__in=params)
                else:
                    q = {f"{key}__{name_attr}__in": params}
                    lessons = lessons.filter(**q)

        sorted_lessons = sorted(
            lessons.distinct(), key=lambda o: collator.getSortKey(o.title)
        )

        paginator = Paginator(sorted_lessons, 8)
        page_number = self.request.GET.get("page")
        page_lessons = paginator.get_page(page_number)

        paginator.elided_page_range = paginator.get_elided_page_range(
            number=page_lessons.number,
            on_each_side=2,
            on_ends=1,
        )

        context["lessons"] = page_lessons

        return context


class LessonListView(LessonListPartialView):
    template_name = "home/lesson_list_view.html"

    def get(self, request, *args, **kwargs):
        new_language = None
        if lang := self.request.GET.get("lang"):
            if lang in VALID_LANG_IDS:
                new_language = lang
                translation.activate(new_language)

        response = super().get(request, *args, **kwargs)

        if new_language:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, new_language)

        return response
