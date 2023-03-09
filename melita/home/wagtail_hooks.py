from django.templatetags.static import static
from django.utils.html import format_html
from taggit.models import Tag
from wagtail import hooks
from wagtail.admin.panels import FieldPanel
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

# --- MODEL ADMIN


class LessonAdmin(ModelAdmin):
    model = Lesson
    menu_icon = "clipboard-list"
    list_display = ("title", "program_type", "language")
    list_filter = ("program_type", "language")
    search_fields = ("title", "program_type__name", "language__name")


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
