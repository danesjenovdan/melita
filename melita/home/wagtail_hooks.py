from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext as _
from taggit.models import Tag
from wagtail import hooks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import (
    ActivityType,
    Duration,
    InstructionMethod,
    Language,
    Lesson,
    Material,
    ProgramType,
    Theme,
)

# --- HELPERS


class LessonButtonHelper(ButtonHelper):
    view_button_classnames = ["button", "button-secondary", "button-small"]

    def view_button(self, obj):
        return {
            "url": reverse("lesson", kwargs={"id": obj.id, "slug": slugify(obj.title)}),
            "label": _("View live"),
            "classname": self.finalise_classname(self.view_button_classnames),
            "title": _("View live"),
        }

    def get_buttons_for_obj(
        self, obj, exclude=None, classnames_add=None, classnames_exclude=None
    ):
        btns = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude
        )
        if "view" not in (exclude or []):
            btns.append(self.view_button(obj))
        return btns


# --- MODEL ADMIN


class LessonAdmin(ModelAdmin):
    model = Lesson
    menu_icon = "clipboard-list"
    list_display = ("title", "program_type", "language")
    list_filter = ("program_type", "language")
    search_fields = ("title", "program_type__name", "language__name")
    button_helper_class = LessonButtonHelper


lesson_admin = LessonAdmin()


class ProgramTypeAdmin(ModelAdmin):
    model = ProgramType
    menu_icon = "list-ul"
    list_display = ("name",)


class LanguageAdmin(ModelAdmin):
    model = Language
    menu_icon = "list-ul"
    list_display = ("name", "code")


class ThemeAdmin(ModelAdmin):
    model = Theme
    menu_icon = "list-ul"
    list_display = ("name",)


class DurationAdmin(ModelAdmin):
    model = Duration
    menu_icon = "list-ul"
    list_display = ("name",)


class InstructionMethodAdmin(ModelAdmin):
    model = InstructionMethod
    menu_icon = "list-ul"
    list_display = ("name",)


class MaterialAdmin(ModelAdmin):
    model = Material
    menu_icon = "list-ul"
    list_display = ("name",)


class ActivityTypeAdmin(ModelAdmin):
    model = ActivityType
    menu_icon = "list-ul"
    list_display = ("name",)


class TagAdmin(ModelAdmin):
    model = Tag
    menu_icon = "tag"
    list_display = ("name", "slug")
    search_fields = ("name",)
    Tag.panels = [FieldPanel("name")]


class LessonsGroup(ModelAdminGroup):
    menu_label = "Lessons"
    menu_icon = "folder-open-inverse"
    menu_order = 200
    items = (
        LessonAdmin,
        ProgramTypeAdmin,
        LanguageAdmin,
        ThemeAdmin,
        DurationAdmin,
        InstructionMethodAdmin,
        MaterialAdmin,
        ActivityTypeAdmin,
        TagAdmin,
    )


modeladmin_register(LessonsGroup)


# --- HOOKS


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/custom_admin.css")
    )


class UserbarEditLessonItem:
    def render(self, request):
        if "lesson" not in request.resolver_match.url_name:
            return ""

        try:
            lesson_id = request.resolver_match.kwargs["id"]
        except KeyError:
            return ""

        if not lesson_id:
            return ""

        edit_url = lesson_admin.url_helper.get_action_url("edit", lesson_id)
        return format_html(
            """
            <li class="w-userbar__item " role="presentation">
                <a href="{}" target="_parent" role="menuitem" tabindex="-1">
                    <svg class="icon icon-edit w-action-icon" aria-hidden="true"><use href="#icon-edit"></use></svg>
                    Edit this lesson
                </a>
            </li>
            """,
            edit_url,
        )


@hooks.register("construct_wagtail_userbar")
def add_edit_lesson_item(request, items):
    return items.insert(1, UserbarEditLessonItem())
